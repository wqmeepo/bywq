from apscheduler.schedulers.blocking import BlockingScheduler
import os, json, logging
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

    def jsonParse(self):
        with open(self.config_path + '\\taskconfig.json', 'r', encoding='utf-8')as fp:
            json_data = json.load(fp)
        return json_data

    def jobStart(self, excute_path):
        print(excute_path + '-----start')
        print(type(excute_path))

    def jobEnd(self, excute_path):
        print(excute_path + '-----end')

    def jobStartGenerator(self):
        json_data = self.jsonParse()
        scheduler = BlockingScheduler(jobstores=self.job_stores, executors=self.executors,
                                      job_defaults=self.job_defaults)
        for data in json_data:
            if json_data[data]['starttatus'] == 'on' or 'ON':
                scheduler.add_job(self.jobStart, trigger='cron', args=(json_data[data]['taskpath'],),
                                  id=json_data[data]['taskname'] + ' start',
                                  day_of_week='mon-fri',
                                  hour=json_data[data]['starthour'],
                                  minute=json_data[data]['startmin'],
                                  jitter=1)
        try:
            print('job_start--begin')
            scheduler.start()
        except SystemExit:
            print('job_start--faild')
            exit()

    def jobEndGenerator(self):
        json_data = self.jsonParse()
        scheduler = BlockingScheduler(jobstores=self.job_stores, executors=self.executors,
                                      job_defaults=self.job_defaults)
        for data in json_data:
            if json_data[data]['endstatus'] == 'on' or 'ON':
                scheduler.add_job(self.jobEnd, trigger='cron', args=(json_data[data]['taskpath'],),
                                  id=json_data[data]['taskname'] + ' end',
                                  day_of_week='mon-fri',
                                  hour=json_data[data]['endhour'],
                                  minute=json_data[data]['endmin'],
                                  jitter=1)
        try:
            print('job_end--begin')
            scheduler.start()
        except SystemExit:
            print('job_end--faild')
            exit()


if __name__ == '__main__':
    config_path = os.getcwd()
    print(config_path)
    auto_maintenance = AutoMaintenance(config_path)
    auto_maintenance.jobStartGenerator()
    auto_maintenance.jobEndGenerator()
