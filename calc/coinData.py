import logging

import numpy
import talib

import okex.futures_api as future
from model.KlineModel import KlineModel

futureAPI = future.FutureAPI('', '', '', True)


class MAApi:
    @staticmethod
    def getMa5(closes):
        logging.getLogger(__name__).info('开始计算ma5')
        ma5 = talib.MA(closes, timeperiod=5, matype=0)
        logging.getLogger(__name__).info('计算完成')
        return ma5

    @staticmethod
    def getMa10(closes):
        logging.getLogger(__name__).info('开始计算ma10')
        ma10 = talib.MA(closes, timeperiod=10, matype=0)
        logging.getLogger(__name__).info('计算完成')
        return ma10

    @staticmethod
    def getMa20(closes):
        logging.getLogger(__name__).info('开始计算ma20')
        ma20 = talib.MA(closes, timeperiod=20, matype=0)
        logging.getLogger(__name__).info('计算完成')
        return ma20

    @staticmethod
    def getMa30(closes):
        logging.getLogger(__name__).info('开始计算ma30')
        ma30 = talib.MA(closes, timeperiod=30, matype=0)
        logging.getLogger(__name__).info('计算完成')
        logging.getLogger(__name__).info('计算完成')
        return ma30

    @staticmethod
    def getMa40(closes):
        logging.getLogger(__name__).info('开始计算ma40')
        ma40 = talib.MA(closes, timeperiod=40, matype=0)
        logging.getLogger(__name__).info('计算完成')
        return ma40

    @staticmethod
    def getMa60(closes):
        logging.getLogger(__name__).info('开始计算ma60')
        ma60 = talib.MA(closes, timeperiod=60, matype=0)
        return ma60

    @staticmethod
    def getMa120(closes):
        logging.getLogger(__name__).info('开始计算ma120')
        ma120 = talib.MA(closes, timeperiod=120, matype=0)
        return ma120


class KlineApi:
    @staticmethod
    def get_kline_1day():
        logging.getLogger(__name__).info('开始获取1day K线数据...')
        result = futureAPI.get_kline('EOS-USD-191227', 86400, start='', end='')
        return map_kline_model(result)

    @staticmethod
    def get_kline_5min():
        logging.getLogger(__name__).info('开始获取5min K线数据...')
        result = futureAPI.get_kline('EOS-USD-191227', 300, start='', end='')
        logging.getLogger(__name__).info('获取完成')
        return map_kline_model(result)


def map_kline_model(data):
    kline_models = []
    for record in data:
        model = KlineModel(record[0], float(record[1]), float(record[2]), float(record[3]), float(record[4]),
                           float(record[5]), float(record[6]))
        kline_models.append(model.__dict__)
    return kline_models


def permutation(kline_day):
    data = kline_day[::-1]
    closes = numpy.array(list(map(lambda x: x['close'], data)))
    ma5data = list(map(lambda x: round(x, 3), MAApi.getMa5(numpy.array(closes)).tolist()))[::-1][0]
    ma10data = list(map(lambda x: round(x, 3), MAApi.getMa10(numpy.array(closes)).tolist()))[::-1][0]
    ma20data = list(map(lambda x: round(x, 3), MAApi.getMa20(numpy.array(closes)).tolist()))[::-1][0]
    ma40data = list(map(lambda x: round(x, 3), MAApi.getMa40(numpy.array(closes)).tolist()))[::-1][0]
    ma120data = list(map(lambda x: round(x, 3), MAApi.getMa120(numpy.array(closes)).tolist()))[::-1][0]
    if (ma5data > ma10data > ma20data > ma40data > ma120data
            and kline_day[0]['low'] < ma10data):
        return 'create_order'
    if ma5data < ma40data:
        return 'sell_order'
