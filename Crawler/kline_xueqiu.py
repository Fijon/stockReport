#-*-coding:utf-8 -*-
import requests
from db import SQLOperation
import config
import json
import random
import time
import log

logger = log.get_logger()

db_operate=SQLOperation()

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
    r = requests.get(url, headers=config.my_headers)
    return r.text

value_format = '("%s", "%s", %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f)'
now = int(round(time.time() * 1000)) 
def line_year(code):
    """
    https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=1553172488945&period=year&type=before&count=-142&indicator=kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy,pe,pb,ps,pcf,market_capital,agt,ggt,balance
    https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=00001&begin=1553174544463&period=year&type=after&count=-29&indicator=kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy,pe,pb,ps,pcf,market_capital,agt,ggt,balance
    """

    url_before = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=%d&period=day&type=before&count=-15&indicator=kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy,pe,pb,ps,pcf,market_capital,agt,ggt,balance" % (code, now)
    #url_after = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=1553174544463&period=day&type=after&count=-1500&indicator=kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy,pe,pb,ps,pcf,market_capital,agt,ggt,balance" % code
    value_before = interview(url_before)
    #value_after = interview(url_after)
    logger.info(value_before)


def done_db(code, value_before, value_after):    
    data_before = json.loads(value_before)
    data_after = json.loads(value_after)
    #获取需要插入的列表类型
    column = (data_before['data']['column'])  
    column.pop(18)
    column.insert(0, 'code')
    column_str = ','.join(column).replace('timestamp', 'day') 

    item_before = data_before['data']['item']
    item_after = data_after['data']['item']
    """
    sql_format_qfq = 'insert into xq_kline_qfq(%s) values '
    sql_format_hfq = 'insert into xq_kline_hfq(%s) values '

    single(code, item_before, column_str, sql_format_qfq)
    single(code, item_after, column_str, sql_format_hfq)
    """
    value_before = []
    value_after = []
    value_before = deal_value(code, item_before)
    value_after = deal_value(code, item_after) 
    sql_qfq = 'insert into xq_kline_qfq(' + column_str +') values ' + ','.join(value_before)
    #print(sql_qfq)
    db_operate.insert_into(sql_qfq)
    sql_hfq = 'insert into xq_kline_hfq(' + column_str +') values ' + ','.join(value_after) 
    #print(sql_hfq)
    db_operate.insert_into(sql_hfq) 
    

def single(code, data_list, column_str, sql_format):
    for item in data_list:
        item.pop(18)
        timeStamp = item[0]/1000 
        timeStr = deal_time(timeStamp)
        deal_item(item)
        sql = sql_format % column_str
        value = value_format % (code,timeStr,item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19],item[20],item[21],item[22],item[23],item[24],item[25],item[26],item[27],item[28],item[29],item[30],item[31],item[32],item[33],item[34],item[35],item[36],item[37],item[38],item[39],item[40],item[41],item[42],item[43])
        insert_sql = sql + value
        print(insert_sql)
        db_operate.insert_into(insert_sql) 



def deal_value(code, item_list):
    value = []
    #value_format = '("%s", "%s", %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)'
    for item in item_list:
        item.pop(18)
        timeStamp = item[0]/1000 
        timeStr = deal_time(timeStamp)
        deal_item(item)
        value_item = value_format % (code,timeStr,item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19],item[20],item[21],item[22],item[23],item[24],item[25],item[26],item[27],item[28],item[29],item[30],item[31],item[32],item[33],item[34],item[35],item[36],item[37],item[38],item[39],item[40],item[41],item[42],item[43])
        value.append(value_item)
    return value
    


def deal_time(timeStamp):
    timeArray = time.localtime(timeStamp)
    timeStr = time.strftime("%Y-%m-%d", timeArray) 
    return timeStr

def deal_item(item):
    for idx in range(len(item)):
        if None == item[idx]:
            item[idx]= 0


def init_data():
    query = "select code from company"
    result = db_operate.select(query)
    print(len(result))
    for code in result:
        print(code[0])
        #line_year(str(code[0]))
        #time.sleep(1)
    
if __name__ == '__main__':
    init_data()