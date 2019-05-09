#!/usr/bin/env python
#-*- coding:utf-8 -*-
import log

logging = log.get_logger()
ONE_BOARD = {'name':'一字板', 'data': [], 'value': 0,  'direction':'', 'size':'', 'color':''}
T_LINE = {'name':'T字线', 'data': [], 'value': 0}
ANTI_T_LINE = {'name':'倒T字线', 'data': [], 'value': 0}
TEN_LINE = {'name':'十字星线', 'data': [], 'value': 0}
LONG_TEN_LINE = {'name':'长十字星线', 'data': [], 'value': 0}
UP_TEN_LINE = {'name':'长上影十字星线', 'data': [], 'value': 0}
DOWN_TEN_LINE = {'name':'长下影十字星线', 'data': [], 'value': 0}


LINE_TYPE_DIRECTION = ['空','上空下影', '上空长下影', '下空上影', '下空长上影', '长上影', '长下影','短线', '长线']
LINE_TYPE_SIZE = ['十字星线','星','小', '中', '大']
LINE_TYPE_SIZE_INDEX = [0,1,2,3,4]

LINE_TYPE_COLOR = ['阴', '阳']

SMALL_START = {'name':'星线', 'data': [0, 0.005], 'value': 0}
EMPTY_SMALL_START={'name':'空星线', 'data': [0], 'value': 0}
UP_EMPTY_SMALL_START = {'name':'空上星线', 'data': [0], 'value': 0}
UP_EMPTY_LONG_SMALL_START = {'name':'空上长星线', 'data': [0], 'value': 0}
DOWN_EMPTY_SMALL_START = {'name':'空下星线', 'data': [0], 'value': 0}
DOWN_EMPTY_LONG_SMALL_START = {'name':'空下长星线', 'data': [0], 'value': 0}

SMALL_LINE = {'name':'小线', 'data': [0.005, 0.02], 'value': 0}
MEDIUM_LINE = {'name':'中线', 'data': [0.02, 0.04], 'value': 0}
LARGEST_LINE = {'name':'大线', 'data': [0.04, 1], 'value': 0}

LINE_GAP = [0.005, 0.02, 0.04]
TEN_LINE_GAP = [0.03, 0.45, 0.55, 0.97]

class KLineAnalysis():
    """
    k线分析
    """

    def __init__(self, code):
        self.__code = code
    
    def setData(self, data):
        """
        K线数据数组列表
        
        """ 
        self.__list_kline = []
        for item in data:
            kline = KLine(item[0], item[1], item[2], item[3])
            self.__list_kline.append(kline)
    
    def oneDayAnalysis(self):
        pass

    def threeDaysAnalysis(self):
        """
        3日k线分析
        """
        length = len(self.__list_kline)
        if length < 3:
            logging.warn(" length of data is not correct, code: %s, length: %d" % (self.__code, length))
            return 
        
        for day in self.__list_kline:
            if day.hl == 0:
                day.form = ONE_BOARD
                break
            # 判断线类型
            entry_ratio = abs(day.oc) / abs(day.hl) 
            if entry_ratio == 0:
                # 十字星线处理
                self.__tenLine(day) 
            else:
                if  entry_ratio <= LINE_GAP[0]:
                    day.form['size'] = LINE_TYPE_SIZE_INDEX[1]
                elif entry_ratio > LINE_GAP[1] and entry_ratio <= LINE_GAP[2]:
                    day.form['size'] = LINE_TYPE_SIZE_INDEX[2]
                elif entry_ratio >= LINE_GAP[2]  and entry_ratio <= LINE_GAP[3]:
                    day.form['size'] = LINE_TYPE_SIZE_INDEX[3]
                else :
                    day.form['size'] = LINE_TYPE_SIZE_INDEX[4]
                # 判断 形态
                self.__lineDirection(day)

            #判断颜色， 阴阳
            if day.oc < 0:
                day.form['value']  = 1
            else: 
                day.form['value'] = -1
            



            print(day)
    
    def __tenLine(self, day):
        """
        十字星线处理计算
        """
        # 上影线与总影线对比
        line_ration = day.ho / day.hl 
        if line_ration <= TEN_LINE_GAP[0]:
            day.form = T_LINE
        elif TEN_LINE_GAP[0] < line_ration and line_ration <= TEN_LINE_GAP[1]:
            day.form = DOWN_TEN_LINE
        elif TEN_LINE_GAP[1] < line_ration and line_ration <= TEN_LINE_GAP[2]:
            day.form = TEN_LINE
        elif TEN_LINE_GAP[2] < line_ration and line_ration <= TEN_LINE_GAP[3]:
            day.form = UP_TEN_LINE
        else :
            day.form = ANTI_T_LINE
        day.form['data'].append(line_ration)
    
    def __lineDirection(self, day):
        """
        判断线方向
        """ 
        day.up_gap = day.high - day.max
        day.down_gap = day.min - day.low 
        if day.up_gap == 0 :
            down_line_ration = day.down_gap / day.hl
            if down_line_ration == 0:
                # 无影线
                day.form = EMPTY_SMALL_START
                day.form['direction'] = LINE_TYPE_DIRECTION[0]
            elif down_line_ration <= 0.5:
                # 上空下影线
                day.form['direction'] = LINE_TYPE_DIRECTION[1]
            else:
                # 上空长下影
                day.form['direction'] = LINE_TYPE_DIRECTION[2]
        else:
            up_line_ration = day.up_gap / day.hl
            if day.down_gap == 0:
                if up_line_ration <= 0.5:
                    #下空上影线
                    day.form['direction'] = LINE_TYPE_DIRECTION[3]
                else:
                    #下空长上影
                   day.form['direction'] = LINE_TYPE_DIRECTION[4]
            else:
                up_ration = day.up_gap /day.oc
                down_ration = day.down_gap / day.oc
                if up_ration >1 :
                    if down_ration > 1:
                        # 长影线
                        day.form['direction'] = LINE_TYPE_DIRECTION[8]
                    else :
                        # 上长影线
                        day.form['direction'] = LINE_TYPE_DIRECTION[5]
                else:
                    if  down_ration < 1:
                        # 短影线
                        day.form['direction'] = LINE_TYPE_DIRECTION[7]
                    else:
                        #下长影线
                        day.form['direction'] = LINE_TYPE_DIRECTION[6] 

            

class KLine():
    """
    """
    def __init__(self, openPri, close, high, low):
        self.openPri = openPri
        self.close = close
        self.high = high
        self.low = low
        self.hl = high - low
        self.hc = high - close
        self.ho = high - openPri
        self.max = max(openPri, close)
        self.min = min(openPri, close)
        self.oc = openPri - close
        self.ol = openPri - low
        self.cl = close - low
        
        
        
    
        
        
