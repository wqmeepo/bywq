import os
import xlwt
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint


#  创建类，支持不同股票代码的数据爬取
class EastMoneySpider(object):
    def __init__(self, stock_code: str, save_path: str):  # 构造函数
        self.stock_code = stock_code
        self.save_path = save_path
        self.smt_url = r'https://data.eastmoney.com/rzrq/detail/'  # 融资融券信息URL
        self.comments_url = r'http://guba.eastmoney.com/list,'  # 评价URL
        self.announcement_url = r'http://guba.eastmoney.com/list,'  # 公告URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
        }

    def smtSpider(self):  # 融资融券数据爬取
        url = self.smt_url + self.stock_code + '.html'
        browser = webdriver.Chrome()
        browser.get(url)
        export_file = xlwt.Workbook(encoding='utf-8')
        sheet = export_file.add_sheet('融资融券数据', cell_overwrite_ok=True)
        try:
            index = 0
            while browser.find_element(By.LINK_TEXT, '下一页').text:
                if index != 0:
                    time.sleep(1)  # 页面加载
                    browser.find_element(By.LINK_TEXT, '下一页').click()  # 点击下一页
                table_source = browser.find_element(By.CSS_SELECTOR, '#rzrq_history_table > table > tbody').text.split(
                    '\n')  # 获取当前页面表格body数据
                table_parse = []
                for column in table_source:
                    table_parse.append(column.split(' '))  # 处理数据，以便插入excel
                for i, p in enumerate(table_parse):
                    for j, q in enumerate(p):
                        sheet.write(i + index, j, q)  # 插入数据进excel
                export_file.save(os.path.join(self.save_path, f'{self.stock_code}融资融券数据.xls'))
                index += len(table_parse)  # 游标信息
        except:
            print(f'代码：{self.stock_code} 融资融券数据已采集完成，请检查')  # 当无下一页时结束采集

    def commentsSpider(self):  # 评价页面解析
        url = self.comments_url + self.stock_code + '.html'
        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(1)  # 页面加载
        total_page = int(browser.find_element(By.CSS_SELECTOR, '.sumpage').text)  # 该页面分页信息是实时计算，需要用selenium获取
        browser.close()  # 关闭browser
        export_file = xlwt.Workbook(encoding='utf-8')
        sheet = export_file.add_sheet('评论数据', cell_overwrite_ok=True)
        index = 0
        try:
            for page in range(total_page):
                print(f'开始第{page + 1}页爬取')
                url = self.comments_url + self.stock_code + f'_{page + 1}.html'  # url拼接
                r = requests.get(url, headers=self.headers)
                time.sleep(randint(4, 7))  # 防止爬取过快被识别爬虫导致封禁
                r.encoding = 'utf-8'  # 编码
                soup = bs(r.text, 'lxml')
                comments_source = soup.select('.all.hs_list .articleh')  # 获取评论区数据
                for i in range(len(comments_source)):  # 插入表格
                    sheet.write(i + index, 0, comments_source[i].select_one('.l1').text)
                    sheet.write(i + index, 1, comments_source[i].select_one('.l2').text)
                    sheet.write(i + index, 2, comments_source[i].select_one('.l3').text)
                    sheet.write(i + index, 3, comments_source[i].select_one('.l4').text)
                    sheet.write(i + index, 4, comments_source[i].select_one('.l5').text)
                export_file.save(os.path.join(self.save_path, f'{self.stock_code}评论数据.xls'))
                index += len(comments_source)  # 游标信息
            print(f'代码：{self.stock_code} 评论数据采集完成')  # 采集完成
        except:
            print(f'代码：{self.stock_code} 评论数据采集失败')  # 采集失败

    def announcementSpider(self):  # 公告页面解析
        url = self.announcement_url + self.stock_code + ',3,f.html'
        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(1)  # 页面加载
        total_page = int(browser.find_element(By.CSS_SELECTOR, '.sumpage').text)  # 该页面分页信息是实时计算，需要用selenium获取
        browser.close()  # 关闭browser
        export_file = xlwt.Workbook(encoding='utf-8')
        sheet = export_file.add_sheet('公告数据', cell_overwrite_ok=True)
        index = 0
        try:
            for page in range(total_page):
                print(f'开始第{page + 1}页爬取')
                url = self.comments_url + self.stock_code + f',3,f_{page + 1}.html'  # url拼接
                print(url)
                r = requests.get(url, headers=self.headers)
                time.sleep(randint(1, 2))  # 防止爬取过快被识别爬虫导致封禁
                r.encoding = 'utf-8'  # 编码
                soup = bs(r.text, 'lxml')
                announcement_source = soup.select('.notice.hs_list .articleh')  # 获取公告区数据
                for i in range(len(announcement_source)):  # 插入表格
                    sheet.write(i + index, 0, announcement_source[i].select_one('.l1').text)
                    sheet.write(i + index, 1, announcement_source[i].select_one('.l2').text)
                    sheet.write(i + index, 2, announcement_source[i].select_one('.l3').text)
                    sheet.write(i + index, 3, announcement_source[i].select_one('.l9').text)
                    sheet.write(i + index, 4, announcement_source[i].select_one('.l5').text)
                export_file.save(os.path.join(self.save_path, f'{self.stock_code}公告数据.xls'))
                index += len(announcement_source)  # 游标信息
            print(f'代码：{self.stock_code} 公告数据采集完成')  # 采集完成
        except:
            print(f'代码：{self.stock_code} 公告数据采集失败')  # 采集失败


if __name__ == '__main__':
    data = EastMoneySpider('002925', r'D:/')
    # data.smtSpider()
    data.commentsSpider()
    # data.announcementSpider()
