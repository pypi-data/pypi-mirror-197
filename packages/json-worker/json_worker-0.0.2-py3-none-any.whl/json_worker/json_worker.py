import datetime
import os
import threading
import traceback
import python_supporter
import time

class ThreadRun:
    def __init__(self, config, work, worker_class, json_worker, inputs_directory, outputs_directory, schedule, schedule_s):
        super().__init__()

        self.config = config
        self.work = work
        self.json_worker = json_worker
        self.schedule = schedule
        self.schedule_s = schedule_s

        self.worker = worker_class(self.config, self.work, self.json_worker, inputs_directory, outputs_directory, schedule_s)

    def run(self):
        if self.schedule_s == None or self.schedule_s == "":
            schedule_s = ""
        elif self.schedule_s == "지금":
            schedule_s = "" 
        else:
            schedule_s = " (" + self.schedule_s +")" 

        self.json_worker.log(f"{self.work['name']}{schedule_s}을 시작합니다.", verbose=True, background_rgb=[204, 255, 255])

        try:
            self.worker.start()

            if not self.worker.running:
                self.json_worker.log(f"{self.work['name']}{schedule_s}을 중지합니다.", verbose=True, background_rgb=[154, 205, 205])
            else:
                self.json_worker.log(f"{self.work['name']}{schedule_s}을 종료합니다.", verbose=True, background_rgb=[154, 205, 205])

            if self.schedule:
                year = self.schedule.get("year")
                month = self.schedule.get("month")
                day = self.schedule.get("day")
                hour = self.schedule.get("hour")
                minute = self.schedule.get("minute")
                second = self.schedule.get("second")
                enable = self.schedule.get("enable")
                if enable:
                    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                    if year != None and month != None and day != None:
                        #logging.debug("internal_mark_schedule_done")
                        self.schedule["internal_mark_schedule_done"] = True
                    elif hour != None and minute != None and second != None:
                        pass
                    elif minute != None and second != None:
                        pass
                    elif second != None:
                        pass
                    else:
                        #logging.debug("internal_mark_schedule_done")
                        self.schedule["internal_mark_schedule_done"] = True

                    internal_mark_work_done = True
                    if self.work.get("schedules") and self.work.get("schedules").get("enable"):
                        for schedule in self.work["schedules"]["schedules"]:
                            if schedule.get("enable"):
                                if not schedule.get("internal_mark_schedule_done"):
                                    internal_mark_work_done = False
                                    break
                        if internal_mark_work_done:
                            #logging.debug(self.work)
                            #logging.debug("internal_mark_work_done")
                            self.work["internal_mark_work_done"] = True
            else:
                #logging.debug("internal_mark_work_done")
                self.work["internal_mark_work_done"] = True
        except BaseException as e:
            self.json_worker.log(traceback.format_exc())
            #logging.debug(traceback.format_exc())
            
            if not self.worker.running:
                self.json_worker.log(f"{self.work['name']}{schedule_s}을 중지합니다.", verbose=True, background_rgb=[154, 205, 205])
            else:
                self.json_worker.log(f"{self.work['name']}{schedule_s}을 종료합니다.", verbose=True, background_rgb=[154, 205, 205])

            #logging.debug("internal_mark_work_done")
            self.work["internal_mark_work_done"] = True

class JsonWorker:
    ##title = "작업 봇"
    ##version = "0.8"

    '''
    @classmethod
    def get_id_and_title_and_version_and_default_setting_text_and_manual(cls):
        return WorkBot.concrete_work_class.id, WorkBot.concrete_work_class.title, WorkBot.concrete_work_class.version, WorkBot.concrete_work_class.default_setting_text, WorkBot.concrete_work_class.manual
        
    @classmethod
    def config_after_load(cls, config, inputs_directory, outputs_directory, models_directory):
        WorkBot.concrete_work_class.config_after_load(config, inputs_directory, outputs_directory, models_directory)

    @classmethod
    def config_before_start(cls, config, inputs_directory, outputs_directory, models_directory):
        WorkBot.concrete_work_class.config_before_start(config, inputs_directory, outputs_directory, models_directory)
    '''
    
    def __init__(self, config, worker_class, inputs_directory, outputs_directory, stop_callback, end_callback, log_callback):
        super().__init__()
        self.title = "작업 봇"
        self.config = config
        self.worker_class = worker_class
        self.inputs_directory = inputs_directory
        self.outputs_directory = outputs_directory
        self.stop_callback = stop_callback
        self.end_callback = end_callback
        self.log_callback = log_callback

        self.running = True
        
        self.thread_runs = []
        self.threads = []

        ##python_supporter.logging_lib.basic_config(app.define_logging_level.level, os.path.join(self.outputs_directory, "log.txt"))

    #def start(self):
    #    self.stop_callback()

    def start(self):
        self.running = True

        self.log(f"{self.title}을 시작합니다.", verbose=True, background_rgb=[204, 255, 255])
        if self.config.get("speak_start_log"):
            python_supporter.tts.speak(f"{self.title}을 시작합니다.")
                    
        message = "활성 작업 리스트입니다."
        self.log(message)
        for work in self.config["works"]:
            name = work["name"]
            enable = work["enable"]
            if enable:
                message = f"{name}"
                self.log(message)
                if work.get("schedules") and work.get("schedules").get("enable"):
                    for schedule in work.get("schedules").get("schedules"):
                        year = schedule.get("year")
                        month = schedule.get("month")
                        day = schedule.get("day")
                        hour = schedule.get("hour")
                        minute = schedule.get("minute")
                        second = schedule.get("second")
                        enable = schedule.get("enable")
                        if enable:
                            dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                            if year != None and month != None  and day != None :
                                schedule_dt = datetime.datetime(year, month, day, hour, minute, second)
                                schedule_s = schedule_dt.strftime('%Y-%m-%d %H:%M:%S')
                                if schedule_dt < dt:
                                    schedule_s = "지난 시간"
                            elif hour != None and minute != None and second != None :
                                schedule_dt = dt.replace(hour=hour, minute=minute, second=second)
                                schedule_s = "매 " + schedule_dt.strftime('%H시 %M분 %S초')
                                schedule_s = schedule_s + " 마다"
                            elif minute != None and second != None :
                                schedule_dt = dt.replace(minute=minute, second=second)
                                schedule_s = "매 " + schedule_dt.strftime('%M분 %S초')
                                schedule_s = schedule_s + " 마다"
                            elif second != None :
                                schedule_dt = dt.replace(second=second)
                                schedule_s = "매 " + schedule_dt.strftime('%S초')
                                schedule_s = schedule_s + " 마다"
                            else:
                                schedule_s = "지금"

                            message = f"    {schedule_s}"
                            self.log(message)
                else:
                    schedule_s = "지금"
                    enable = work["enable"]
                    if enable:
                        message = f"    {schedule_s}"
                        self.log(message)

        while True:
            for work in self.config["works"]:
                if not self.running:
                    break
                if work["enable"] and not work.get("internal_mark_work_no_more_run"):
                    if work.get("schedules") and work.get("schedules").get("enable"):
                        for schedule in work["schedules"]["schedules"]:
                            if not self.running:
                                break
                            if schedule["enable"] and not schedule.get("internal_mark_schedule_no_more_run"):
                                year = schedule.get("year")
                                month = schedule.get("month")
                                day = schedule.get("day")
                                hour = schedule.get("hour")
                                minute = schedule.get("minute")
                                second = schedule.get("second")

                                dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                                if year != None and month != None and day != None:
                                    if year == dt.year  and month == dt.month and day == dt.day and hour == dt.hour and minute == dt.minute and second == dt.second: 
                                        schedule["internal_mark_schedule_no_more_run"] = True
                                        schedule_dt = datetime.datetime(year, month, day, hour, minute, second)
                                        schedule_s = schedule_dt.strftime('%Y-%m-%d %H:%M:%S')
                                        thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, schedule, schedule_s)
                                        thread = threading.Thread(target=thread_run.run, args=[])
                                        thread.daemon = True
                                        thread.start()
                                        self.thread_runs.append(thread_run)
                                        self.threads.append(thread)
                                        if self.config["sequence"]:
                                            thread.join()
                                    else: #지난 시간
                                        schedule_dt = datetime.datetime(year, month, day, hour, minute, second)
                                        if schedule_dt < dt:
                                            schedule["internal_mark_schedule_no_more_run"] = True
                                            schedule["internal_mark_schedule_done"] = True

                                            internal_mark_work_done = True
                                            if work.get("schedules") and work.get("schedules").get("enable"):
                                                for schedule in work["schedules"]["schedules"]:
                                                    if schedule.get("enable"):
                                                        if not schedule.get("internal_mark_schedule_done"):
                                                            internal_mark_work_done = False
                                                            break
                                                if internal_mark_work_done:
                                                    #logging.debug(work)
                                                    #logging.debug("internal_mark_work_done")
                                                    work["internal_mark_work_done"] = True
                                elif hour != None and minute != None and second != None:
                                    if hour == dt.hour and minute == dt.minute and second == dt.second:
                                        if dt.year != schedule.get("internal_mark_schedule_no_more_run_year") or dt.month != schedule.get("internal_mark_schedule_no_more_run_month") or dt.day != schedule.get("internal_mark_schedule_no_more_run_day"):
                                            schedule["internal_mark_schedule_no_more_run_year"] = dt.year
                                            schedule["internal_mark_schedule_no_more_run_month"] = dt.month
                                            schedule["internal_mark_schedule_no_more_run_day"] = dt.day
                                            schedule_dt = dt.replace(hour=hour, minute=minute, second=second)
                                            schedule_s = "매 " + schedule_dt.strftime('%H시 %M분 %S초')
                                            schedule_s = schedule_s + " 마다"
                                            thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, schedule, schedule_s)
                                            thread = threading.Thread(target=thread_run.run, args=[])
                                            thread.daemon = True
                                            thread.start()
                                            self.thread_runs.append(thread_run)
                                            self.threads.append(thread)
                                            if self.config["sequence"]:
                                                thread.join()
                                elif minute != None and second != None:
                                    if minute == dt.minute and second == dt.second:
                                        if dt.year != schedule.get("internal_mark_schedule_no_more_run_year") or dt.month != schedule.get("internal_mark_schedule_no_more_run_month") or dt.day != schedule.get("internal_mark_schedule_no_more_run_day") or dt.hour != schedule.get("internal_mark_schedule_no_more_run_hour"):
                                            schedule["internal_mark_schedule_no_more_run_year"] = dt.year
                                            schedule["internal_mark_schedule_no_more_run_month"] = dt.month
                                            schedule["internal_mark_schedule_no_more_run_day"] = dt.day
                                            schedule["internal_mark_schedule_no_more_run_hour"] = dt.hour
                                            schedule_dt = dt.replace(minute=minute, second=second)
                                            schedule_s = "매 " + schedule_dt.strftime('%M분 %S초')
                                            schedule_s = schedule_s + " 마다"
                                            thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, schedule, schedule_s)
                                            thread = threading.Thread(target=thread_run.run, args=[])
                                            thread.daemon = True
                                            thread.start()
                                            self.thread_runs.append(thread_run)
                                            self.threads.append(thread)
                                            if self.config["sequence"]:
                                                thread.join()
                                elif second != None:
                                    if second == dt.second:
                                        if dt.year != schedule.get("internal_mark_schedule_no_more_run_year") or dt.month != schedule.get("internal_mark_schedule_no_more_run_month") or dt.day != schedule.get("internal_mark_schedule_no_more_run_day") or dt.hour != schedule.get("internal_mark_schedule_no_more_run_hour") or dt.minute != schedule.get("internal_mark_schedule_no_more_run_minute"):
                                            schedule["internal_mark_schedule_no_more_run_year"] = dt.year
                                            schedule["internal_mark_schedule_no_more_run_month"] = dt.month
                                            schedule["internal_mark_schedule_no_more_run_day"] = dt.day
                                            schedule["internal_mark_schedule_no_more_run_hour"] = dt.hour
                                            schedule["internal_mark_schedule_no_more_run_minute"] = dt.minute
                                            schedule_dt = dt.replace(second=second)
                                            schedule_s = "매 " + schedule_dt.strftime('%S초')
                                            schedule_s = schedule_s + " 마다"
                                            thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, schedule, schedule_s)
                                            thread = threading.Thread(target=thread_run.run, args=[])
                                            thread.daemon = True
                                            thread.start()
                                            self.thread_runs.append(thread_run)
                                            self.threads.append(thread)
                                            if self.config["sequence"]:
                                                thread.join()
                                else:
                                    schedule["internal_mark_schedule_no_more_run"] = True
                                    schedule_s = "지금"
                                    thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, schedule, schedule_s)
                                    thread = threading.Thread(target=thread_run.run, args=[])
                                    thread.daemon = True
                                    thread.start()
                                    self.thread_runs.append(thread_run)
                                    self.threads.append(thread)
                                    if self.config["sequence"]:
                                        thread.join()

                        internal_mark_work_no_more_run = True
                        for schedule in work["schedules"]["schedules"]:
                            if schedule.get("enable"):
                                if not schedule.get("internal_mark_schedule_no_more_run"):
                                    internal_mark_work_no_more_run = False
                                    break
                        if internal_mark_work_no_more_run:
                            work["internal_mark_work_no_more_run"] = True
                    else:
                        work["internal_mark_work_no_more_run"] = True
                        schedule_s = "지금"
                        thread_run = ThreadRun(self.config, work, self.worker_class, self, self.inputs_directory, self.outputs_directory, None, schedule_s)
                        thread = threading.Thread(target=thread_run.run, args=[])
                        thread.daemon = True
                        thread.start()
                        self.thread_runs.append(thread_run)
                        self.threads.append(thread)
                        if self.config["sequence"]:
                            thread.join()
                    
            #logging.debug("========")
            #logging.debug(self.threads)
            for work in self.config["works"]:
                #logging.debug("------")
                #logging.debug(json.dumps(work, indent=4))
                pass

            if not self.running:
                for thread in self.threads:
                    thread.join()
                self.stop_callback()
                self.log(f"{self.title}을 중지합니다.", verbose=True, background_rgb=[154, 205, 205])
                if self.config.get("speak_stop_log"):
                    python_supporter.tts.speak(f"{self.title}을 중지합니다.")
                break

            all_done = True
            for work in self.config["works"]:
                if work["enable"]:
                    #logging.debug(work.get("internal_mark_work_done"))
                    if not work.get("internal_mark_work_done"):   
                        all_done = False
            if all_done:
                if self.end_callback:
                    self.end_callback()
                self.log(f"{self.title}을 종료합니다.", verbose=True, background_rgb=[154, 205, 205])
                if self.config.get("speak_stop_log"):
                    ai_supporter.tts.speak(f"{self.title}을 종료합니다.")
                break

            time.sleep(0.1)

    def log(self, message, verbose=True, background_rgb=[255, 255, 255]):  
        if self.log_callback:
            self.log_callback(message, verbose, background_rgb)
        else:
            dt = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
            text = message + ", " + dt.strftime('%Y-%m-%d %H:%M:%S')
            print(text)
       
    def stop(self):
        self.running = False

        for thread_run in self.thread_runs:
            thread_run.worker.stop()

if __name__ == "__main__":
    import app
    
    current_py_file_path = os.path.dirname(os.path.realpath(__file__))
    inputs_directory = current_py_file_path+"/../inputs"
    outputs_directory = current_py_file_path+"/../outputs"
    config = python_supporter.config.load_config_from_file(inputs_directory+"/config.json")
    worker_class = app.work.static_site_article_notification.static_site_article_notification.StaticSiteArticleNotification
    #print(inputs_directory) #C:\Users\Administrator\Desktop\static-site-article-notification-app-main\app\app/../inputs
    #print(outputs_directory) #C:\Users\Administrator\Desktop\static-site-article-notification-app-main\app\app/../outputs

    config = python_supporter.config.load_config_from_file(os.path.join(inputs_directory, "config.json"))
    json_worker = JsonWorker(config, worker_class, inputs_directory, outputs_directory)

    json_worker.start()
