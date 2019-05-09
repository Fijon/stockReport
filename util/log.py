import logging
import os


import logging,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #获取上级目录的绝对路径
log_dir = BASE_DIR + '/log'
log_path = log_dir +'/record.log'

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_logger():
    mkdir(log_dir)
    #创建一个文件流并设置编码utf8
    fh = logging.FileHandler(log_path,encoding='utf-8') 
     #获得一个logger对象，默认是root
    logger = logging.getLogger()
     #设置最低等级debug
    logger.setLevel(logging.INFO) 
    fm = logging.Formatter("%(message)s")  #设置日志格式
    logger.addHandler(fh) #把文件流添加进来，流向写入到文件
    fh.setFormatter(fm) #把文件流添加写入格式
    return logger

logger = get_logger()

logger.warn("testOne")