#-*-coding:utf-8 -*-
from urllib  import request
import requests
import datetime
import os
import calendar 
import sys
from db import SQLOperation
import json
import random
import time

#http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq2016&param=hk00001,day,2016-01-01,2017-12-31,640,qfq&r=0.749340051711368
#http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq2014&param=hk00001,day,2014-01-01,2015-12-31,640,qfq&r=0.21642513231507565
#http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00001,day,,,320,qfq&r=0.3271787747744508
#http://web.ifzq.gtimg.cn/other/klineweb/klineWeb/weekTrends?code=hk00001&type=qfq&_var=trend_qfq&r=0.6838330831530213
#http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_monthqfq&param=hk00001,month,,,320,qfq&r=0.4003386476204329
#
#
"""
http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk80737,day,,,320,qfq
http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq2016&param=hk00001,day,2016-01-01,2017-12-31,640,qfq
http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayhfq&param=hk00001,day,,,320,hfq
http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayhfq2016&param=hk00001,day,2016-01-01,2017-12-31,640,hfq
"""

"""
https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=3000&order=asc&orderby=code&order_by=symbol&market=HK&type=hk
"""
db_operate = SQLOperation()

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

company_format_url = "https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=3000&order=asc&orderby=code&order_by=symbol&market=HK&type=hk"

def company_message():
    company_str = interview(company_format_url)
    company_data = json.loads(company_str)
    data_array = company_data['data']['list']
    insert_sql = "insert into company(code, name, region, lot_size) values "
    value_format = '("%s", "%s", "%s", %d)'
    value_array = []
    for item in data_array:
        print(item['name'], item['symbol'], item['lot_size'])
        value_array.append(value_format %(item['symbol'],item['name'],'HK',  item['lot_size']))
    value_str = ','.join(value_array)
    sql = insert_sql + value_str
    db_operate.insert_into(sql)



def qfq_year_add(code, qfq_array, isTrue):
    insert_sql = ''
    if isTrue:
        insert_sql = "insert into kline_qfq(code, day, opening_price, closing_price, min_price, max_price, volume, turnover) values "
    else:
        insert_sql = "insert into kline_hfq(code, day, opening_price, closing_price, min_price, max_price, volume, turnover) values "
    value_format = '("%s", "%s",%.3f,%.3f,%.3f,%.3f,%.3f,%.3f)'
    value_array = []
    for item in qfq_array:
        value =  value_format % (code, item[0], float(item[1]),float(item[2]),float(item[3]),float(item[4]),float(item[5]),float(item[8]))
        value_array.append(value)
    value_str = ','.join(value_array)
    sql = insert_sql + value_str
    print(len(value_array))
    db_operate.insert_into(sql)


def day_download():
    pass


def fdays_download():
    pass

year_format_qfq = 'http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=%s,day,,%s,%d,qfq'
year_format_hfq = 'http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayhfq&param=%s,day,%s,%s,%d,hfq'

def year_download(code, begin, end):
    qfq_url = year_format_qfq % (code, end, 1500)
    hfq_url = year_format_hfq % (code, begin, end, 1500)
    print(qfq_url)
    print(hfq_url)
    page = request.urlopen(qfq_url).read()
    htmlcode = page.decode('utf-8')
    data = json.loads(htmlcode.split("=")[1])
    qfq_dict = data['data'][code]
    if 'qfqday' in qfq_dict:
        qfq_array = qfq_dict['qfqday']
        qfq_year_add(code[2:len(code)], qfq_array, True)
    
    page = request.urlopen(hfq_url).read()
    htmlcode = page.decode('utf-8')
    data = json.loads(htmlcode.split("=")[1])
    hfq_dict = data['data'][code]
    if 'hfqday' in hfq_dict:
        hfq_array = hfq_dict['hfqday']
        qfq_year_add(code[2:len(code)], hfq_array, False)

def interview(url):
    """
    req = request.Request(url)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
    req.add_header('Accept', "application/json; charset=utf-8")
    req.add_header('Accept-Encoding', 'gzip, deflate, br')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.9')
    req.add_header('Cache-Control','max-age=0')
    req.add_header('Connection',' keep-alive')
    req.add_header('Cookie','_ga=GA1.2.1846631486.1552315415; device_id=5cad983f8c11ac55ac642b1b22221418; s=dv12689hpk; xq_a_token=32c802a4240da641d66417001a2db2647ff13a9b; xqat=32c802a4240da641d66417001a2db2647ff13a9b; xq_r_token=6e94c79e2514bee7285c4793e0b85ad7571e1a3e; xq_token_expire=Fri%20Apr%2005%202019%2022%3A43%3A56%20GMT%2B0800%20(CST); xq_is_login=1; u=1917053402; bid=a54590804348668b7dc490d782c81d30_jt4gq6po; __utmz=1.1552315770.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAANeGFWZBJAAAxTZlOhUlqImPXNEH; Hm_lvt_1db88642e346389874251b5a1eded6e3=1552315416,1552814978,1552999986; _gid=GA1.2.310396720.1552999987; __utmc=1; snbim_minify=true; __utma=1.1846631486.1552315415.1553000040.1553006026.4; __utmb=1.1.10.1553006026; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1553006044')
    req.add_header('Host','xueqiu.com')
    req.add_header('Upgrade-Insecure-Requests','1') 
    req.add_header('Content-Type','application/json; charset=utf-8')
    page = request.urlopen(req).read()
    """
    headers = {'User-Agent': random.choice(my_headers)}
    r = requests.get(url, headers=headers) 
    return r.text



def ini_year_data(code): 
    now_time = datetime.datetime.now()
    strTime_end = now_time.strftime('%Y-%m-%d')
    begin_time = now_time + datetime.timedelta(-1500)
    strTime_begin = begin_time.strftime("%Y-%m-%d")
    year_download('hk'+code, strTime_begin, strTime_end)
    

def init_company_data():
    company_message()

if __name__ == '__main__':
    ini_year_data('00001')
    #init_company_data()
    """
    sql = "select code from company"
    result = db_operate.select(sql)
    for item in result:
        ini_year_data(item[0])
        time.sleep(1)
    """