# -*- coding: utf-8 -*-

# 收集到的常用Header
import configparser
my_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "xq_a_token=d729f0d1dafe5a6fa97a4479a398bee96ad40daf; xq_a_token.sig=E_oWkIRXLzY9jShEop_cL1Cho-4; xq_r_token=82de8adc358f46d286f033ff8a0403310e56c969; xq_r_token.sig=pWkiZQ7anInrwuRDKG7nXTznEb8; _ga=GA1.2.1290549653.1557243827; _gid=GA1.2.649192837.1557243827; u=171557243826953; Hm_lvt_1db88642e346389874251b5a1eded6e3=1557243828; device_id=89a37967431e6d79cede658aef7a504d; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1557243840",
    "Host": "stock.xueqiu.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}

def get_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    db_host = config.get('DB', 'DB_HOST')
    print(db_host)


    
if __name__ == '__main__':
    config_path = './config/crawler.ini'
    get_config(config_path)