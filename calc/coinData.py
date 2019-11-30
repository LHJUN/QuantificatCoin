import logging

import numpy
import talib
from pyecharts.charts import Line
from pyecharts.options import DataZoomOpts, AxisOpts, TitleOpts

import okex.futures_api as future
from model.KlineModel import KlineModel
from model.user import OrderType

futureAPI = future.FutureAPI('', '', '', True)


class MAApi:
    @staticmethod
    def getMa5(closes):
        ma5 = talib.MA(closes, timeperiod=5, matype=0)
        return ma5

    @staticmethod
    def getMa10(closes):
        ma10 = talib.MA(closes, timeperiod=10, matype=0)
        return ma10

    @staticmethod
    def getMa20(closes):
        ma20 = talib.MA(closes, timeperiod=20, matype=0)
        return ma20

    @staticmethod
    def getMa30(closes):
        ma30 = talib.MA(closes, timeperiod=30, matype=0)
        return ma30

    @staticmethod
    def getMa40(closes):
        ma40 = talib.MA(closes, timeperiod=40, matype=0)
        return ma40

    @staticmethod
    def getMa60(closes):
        ma60 = talib.MA(closes, timeperiod=60, matype=0)
        return ma60

    @staticmethod
    def getMa120(closes):
        ma120 = talib.MA(closes, timeperiod=120, matype=0)
        return ma120


class KlineApi:
    @staticmethod
    def get_kline_1day():
        logging.getLogger(__name__).info('开始获取1day K线数据...')
        result = futureAPI.get_kline('EOS-USD-191227', 86400, start='', end='')
        return map_kline_model(result)

    @staticmethod
    def get_kline_5min(start='', end=''):
        logging.getLogger(__name__).info('开始获取5min K线数据...')
        result = futureAPI.get_kline('EOS-USD-191227', 300, start=start, end=end)
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
    closes = numpy.array(list(map(lambda x: x['close'], kline_day)))
    ma5data = get_current_ma(MAApi.getMa5(closes).tolist())
    ma10data = get_current_ma(MAApi.getMa10(closes).tolist())
    ma20data = get_current_ma(MAApi.getMa20(closes).tolist())
    ma40data = get_current_ma(MAApi.getMa40(closes).tolist())
    ma120data = get_current_ma(MAApi.getMa120(closes).tolist())
    if (ma5data > ma10data > ma20data > ma40data > ma120data
            and kline_day[len(kline_day) - 1]['low'] < ma10data):
        return OrderType.多单
    if ma5data < ma10data < ma20data < ma40data < ma120data and kline_day[len(kline_day) - 1]['high'] > ma10data:
        return OrderType.空单


def draw_ma():
    kline_1day = KlineApi.get_kline_5min()[::-1]
    times = list(map(lambda x: x['timestamp'], kline_1day))[120:]
    closes = numpy.array(list(map(lambda x: x['close'], kline_1day)))
    ma30data = MAApi.getMa30(closes).tolist()[120:]
    ma60data = MAApi.getMa60(closes).tolist()[120:]
    ma120data = MAApi.getMa120(closes).tolist()[120:]
    c = (
        Line()
            .add_xaxis(times)
            .add_yaxis("MA30", ma30data, is_smooth=True)
            .add_yaxis("MA60", ma60data, is_smooth=True)
            .add_yaxis("MA120", ma120data, is_smooth=True)
            .set_global_opts(
            # datazoom_opts=DataZoomOpts(is_show=True, type_='inside'),
            yaxis_opts=AxisOpts(is_scale=True, split_number=12, max_=2.82, min_=2.7),
            title_opts=TitleOpts(title="Line-smooth")
        )
    )
    logging.getLogger().info(c.render())


def get_current_ma(mas):
    return list(mas)[::-1][0]
