from urllib import request
import time
import datetime
import os
import calendar
import xlrd
import pymysql
import sys

url_format = "http://www.hkexnews.hk/reports/sharerepur/documents/SRRPT%s.xls"
DB_HOST = 'mysql.sql122.cdncenter.net'
DB_PORT = 3306
DB_USER='sq_Fijon'
DB_PWD = '*******'
DB_DB = 'sq_Fijon'
FILE_PATH = './report/'

class BuyBackReport():
    def __init__(self):
        pass

    def __str__(self):
        return '公司名称： %s， 公司代码： %s， 认购方式： %s' % (self.name, self.code, self.ord)

class SQLOperation():
    
    def __init__(self, host, user, pwd, db):
        self.db =  pymysql.connect(host = host, user= user, passwd=pwd,db= db)
        self.cursor = self.db.cursor()
    
    def insert_into(self, report):
        sql = "insert into Repurchase(code,company,type_purchase,price,lowestPrice,totalPaid,method,num_purchased,num_purchased_Exchange,proportion_exchange,tradingDate) value(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
        sql = sql % (report.code, report.name, report.ord, report.hight_price, report.lowest_price, report.total_paid, report.method,report.num_purchased, report.num_purchased_exchange, report.proportion_exchange, report.trading_date)
        try:
             # 执行sql语句
             self.cursor.execute(sql)
             # 执行sql语句
             self.db.commit()
        except Exception as  e:
              
             # 发生错误时回滚
             print(e)
             self.db.rollback()
    
    def execite_sql(self, sql):
        
        self.cursor.execute(sql)
        tmp = []
        result = self.cursor.fetchall()
        for row in result:
            print(row)
        


class DownloadReport():
    def __init__(self, path):
        self.path = path
        self.error_list = []
        if not os.path.exists(path):
            os.mkdir(path)

    def download(self, url):
        url_array = url.split('/')

        file_name = self.path + url_array[len(url_array) - 1 ]
        print('path_pre: %s, name: %s' % (self.path, url_array[len(url_array) - 1 ]))
        try:
            request.urlretrieve(url, file_name)
            print("save path: %s" % file_name)
        except:
            self.error_list.append(url)

class ParseReport():
    def __init__(self, path):
        self.path = path

    def parse(self, name):
        wb = xlrd.open_workbook(self.path+ name)
        sheet = wb.sheet_by_index(0)
        row_index = 5
        report_array = []

        while row_index < sheet.nrows:
            report  = BuyBackReport()
            report.name = sheet.cell_value(row_index, 0)
            if len(report.name) <= 0:
                break
            code = sheet.cell_value(row_index, 1)
            report.code = code.zfill(4)
            report.ord = sheet.cell_value(row_index, 2) 
            report.trading_date = sheet.cell_value(row_index, 3)
            report.num_purchased = sheet.cell_value(row_index,4)
            report.hight_price = sheet.cell_value(row_index, 5)
            report.lowest_price = sheet.cell_value(row_index, 6) 
            report.total_paid = sheet.cell_value(row_index, 7) 
            report.method= sheet.cell_value(row_index, 8)  
            report.num_purchased_exchange = sheet.cell_value(row_index, 9) 
            report.proportion_exchange = sheet.cell_value(row_index, 10)
            report_array.append(report)
            row_index += 1
        for tmp in report_array:
            print(tmp)
        return report_array

def init_download(download, parse, sqlOperation):
    url_list = []
    
    day = datetime.date(2019, 2,19)
    now_day = datetime.date(2019, 2,24)
    #download = DownloadReport("./report/")
    #parse = ParseReport('./report/')
    while day < now_day:
        if (day.weekday() == 5 ):
            day = day + datetime.timedelta(2)
            continue
        if (day.weekday() == 6) :
            day = day + datetime.timedelta(1)
            continue
        day_str = day.isoformat().replace('-', '')
        url_request = url_format % day_str
        day = day + datetime.timedelta(1)
        print(url_request)
        url_array = url_request.split('/')
        file_name = url_array[len(url_array) - 1 ]
        download.download(url_request)
        report_array = parse.parse(file_name)
        for report in report_array:
            sqlOperation.insert_into(report)
        time.sleep(1)
    print("==========%s==========" % ' ERROR LIST ')
    for item in download.error_list:
        print(item)

def download_day(download, parse, sqlOperation, day):
    if (day.weekday() < 5 ):
        day_str = day.isoformat().replace('-', '')
        url_request = url_format % day_str
        day = day + datetime.timedelta(1)
        print(url_request)
        url_array = url_request.split('/')
        file_name = url_array[len(url_array) - 1 ]
        download.download(url_request)
        report_array = parse.parse(file_name)
        for report in report_array:
            sqlOperation.insert_into(report)
        time.sleep(1)
    
def test_mysql(sqlOperation):
    sql = 'select * from Repurchase order by tradingDate desc limit 10'
    sqlOperation.execite_sql(sql)
    
def download_day_export():
    sqlOperation = SQLOperation(DB_HOST,DB_USER, DB_PWD,DB_DB)
    download = DownloadReport(FILE_PATH)
    parse = ParseReport(FILE_PATH)
    day = datetime.date.today()
    if day.weekday() >= 5 :
        print("today is weekend, does not any report to install, day: %s" % day.isoformat())
    else:
        download_day(download, parse, sqlOperation, day)

if __name__ == '__main__':
    sqlOperation = SQLOperation(DB_HOST,DB_USER, DB_PWD,DB_DB)
    download = DownloadReport(FILE_PATH)
    parse = ParseReport(FILE_PATH)
    if len(sys.argv) <= 1:
        day = datetime.date.today()
        print("-------------%s-------------" % datetime.datetime.now())
        download_day(download, parse, sqlOperation, day)
        print("====== DOWNLOAD %s END ======" % day)
        
    else:
        init_download(download, parse, sqlOperation)
        print("two")

