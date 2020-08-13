from apscheduler.schedulers.blocking import BlockingScheduler
import os, json, logging, subprocess, time, random
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger


class AutoMaintenance(object):
    def __init__(self, config_path):
        self.job_stores = {  # 设置任务储存器存储方式-内存
            'default': MemoryJobStore(),
        }
        self.executors = {  # 设置执行器线程池进程池
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(10)
        }
        self.job_defaults = {  # 设置最大实例数量
            'coalesce': False,
            'max_instances': 15
        }
        self.config_path = config_path  # 获取配置文件地址
        self.process_list = []  # 用于存储线程

    def jsonParse(self):  # 配置文件读取
        # 配置文件名写死为taskconfig.json
        try:
            with open(self.config_path + '\\taskconfig.json', 'r', encoding='utf-8')as fp:
                json_data = json.load(fp)
        except:
            print('配置文件读取异常，请检查文件是否存在')
            time.sleep(5)
            exit()
        return json_data

    def jobStart(self, *args):  # 获取调度器传来的任务路径
        time.sleep(random.randrange(0, 6))  # 避免任务同时启动造成卡顿
        print(args[1] + ' 任务开始启动')
        self.process_list.append(subprocess.Popen(args[0]))  # 启动子线程并将线程存储在processlist里

    def jobEnd(self):  # 关闭任务
        print('任务关闭')
        for process in self.process_list:  # 遍历processlist并杀掉所有线程
            process.kill()
            time.sleep(2)  # 避免任务关闭太快
        self.process_list = []  # 清空processlist

    def jobGenerator(self):  # 任务调度器
        json_data = self.jsonParse()  # 获取配置文件
        # 设置APScheduler执行配置
        scheduler = BlockingScheduler(jobstores=self.job_stores, executors=self.executors,
                                      job_defaults=self.job_defaults)
        for data in json_data:
            if json_data[data]['startstatus'] == 'on':  # 判断任务是否启动
                # 启动调度器设置，写死为按每周1-周五执行，小时与分钟支持配置文件配置
                trigger_start = CronTrigger(
                    day_of_week='mon-fri',
                    hour=json_data[data]['starthour'],
                    minute=json_data[data]['startmin'], )
                scheduler.add_job(self.jobStart, trigger_start,
                                  args=(json_data[data]['taskpath'], json_data[data]['taskname']),
                                  id=json_data[data]['taskname'] + ' start',
                                  )
                # 关闭调度器设置
                trigger_stop = CronTrigger(
                    day_of_week='mon-fri',
                    hour=json_data[data]['endhour'],
                    minute=json_data[data]['endmin'], )
                scheduler.add_job(self.jobEnd, trigger_stop)
        try:  # 获取调度器启动异常
            print('任务监控开始，目前监视中的任务有：\n')
            for data in json_data:
                if json_data[data]['startstatus'] == 'on':  # 判断任务是否启动
                    print('{0}、{1},启动时间：{2}:{3},关闭时间：{4}:{5}'.format(json_data[data]['taskid'],
                                                                     json_data[data]['taskname'],
                                                                     json_data[data]['starthour'],
                                                                     json_data[data]['startmin'],
                                                                     json_data[data]['endhour'],
                                                                     json_data[data]['endmin']))
            scheduler.start()
        except SystemExit:
            print('调度器启动失败')
            exit()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    config_path = os.getcwd()  # 获取当前脚本所在目录，即配置文件与脚本文件同目录
    print('当前脚本所在目录为：' + config_path)
    auto_maintenance = AutoMaintenance(config_path)
    auto_maintenance.jobGenerator()
