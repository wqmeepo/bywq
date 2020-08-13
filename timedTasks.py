from apscheduler.schedulers.blocking import BlockingScheduler
import os, json, logging, subprocess, time
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class AutoMaintenance(object):
    def __init__(self, config_path):
        self.job_stores = {
            'default': MemoryJobStore(),
        }
        self.executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(10)
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 5
        }
        self.config_path = config_path
        self.process_list = []

    def jsonParse(self):
        with open(self.config_path + '\\taskconfig.json', 'r', encoding='utf-8')as fp:
            json_data = json.load(fp)
        return json_data

    def jobStart(self, *args):
        print(args[1] + ' 任务启动')
        self.process_list.append(subprocess.Popen(args[0]))

    def jobEnd(self):
        print('任务进程关闭开始')
        for process in self.process_list:
            process.kill()
            time.sleep(2)
        self.process_list = []

    def jobStartGenerator(self):
        json_data = self.jsonParse()
        scheduler = BlockingScheduler(jobstores=self.job_stores, executors=self.executors,
                                      job_defaults=self.job_defaults)
        for data in json_data:
            if json_data[data]['startstatus'] == 'on' or 'ON':
                scheduler.add_job(self.jobStart, trigger='cron',
                                  args=(json_data[data]['taskpath'], json_data[data]['taskname']),
                                  id=json_data[data]['taskname'] + ' start',
                                  day_of_week='mon-fri',
                                  hour=json_data[data]['starthour'],
                                  minute=json_data[data]['startmin'],
                                  jitter=3)
                scheduler.add_job(self.jobEnd, trigger='cron',
                                  day_of_week='mon-fri',
                                  hour=json_data[data]['endhour'],
                                  minute=json_data[data]['endmin'], )
        try:
            print('任务监控开始')
            scheduler.start()
        except SystemExit:
            print('任务监控结束')
            exit()


if __name__ == '__main__':
    config_path = os.getcwd()
    print(config_path)
    auto_maintenance = AutoMaintenance(config_path)
    auto_maintenance.jobStartGenerator()
