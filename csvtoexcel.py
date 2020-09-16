import os, json, time, csv
import xlwt


class CsvToExcel(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def jsonParse(self):
        # 配置文件名写死为taskconfig.json
        try:
            with open(self.config_path + '\\csvtoexcel.json', 'r', encoding='utf-8')as fp:
                json_data = json.load(fp)
        except:
            print('配置文件读取异常，请检查文件是否存在')
            time.sleep(5)
            exit()
        return json_data

    def csvToExcel(self):
        self.jsonParse()
        csv_path, excel_path = self.jsonParse()['csvpath'], self.jsonParse()['excelpath']
        #  判断路径是否存在，不存在就创建
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)
        if not os.path.exists(excel_path):
            os.mkdir(excel_path)

        # 开始处理csv文件到excel文件
        csv_list = os.listdir(csv_path)  # 获取csv文件夹下文件列表
        for csv_list_file in csv_list:
            excel_file = xlwt.Workbook()  # 创建excel文件
            excel_sheet = excel_file.add_sheet(csv_list_file)  # 按csv文件创建excel sheet名
            with open(csv_path + csv_list_file) as csv_file:  # 获取csv文件内容
                csv_reader = csv.reader(csv_file)
                l = 0  # 行
                print(csv_list_file + '执行转换中')
                for line in csv_reader:  # 获取单行信息
                    r = 0  # 列
                    for i in line:
                        excel_sheet.write(l, r, i)  # 按行列写入excel
                        r += 1
                    l += 1
            excel_file_name = csv_list_file.split('.')[0]
            excel_file.save(excel_path + excel_file_name + '.xls')
            print('{0}{1}'.format(csv_list_file, '已转换完成'))


if __name__ == '__main__':
    time_start = time.perf_counter()
    config_path = os.getcwd()  # 获取当前脚本所在目录，即配置文件与脚本文件同目录
    csv_to_excel = CsvToExcel(config_path)
    csv_to_excel.csvToExcel()
    time_stop = time.perf_counter()
    print('花费了{0}秒'.format(time_stop-time_start))
