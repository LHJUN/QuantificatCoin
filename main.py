import numpy
from pyecharts.charts import Line
from pyecharts.options import DataZoomOpts, AxisOpts, TitleOpts

from calc.coinData import KlineApi, MAApi, permutation, draw_ma
import logging

from model.order import Order
from model.user import User, OrderType

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test():
    flag = 0
    kline5min = []
    t_kline5min = KlineApi.get_kline_3min()
    for i in range(0, 6):
        t_kline5min = KlineApi.get_kline_3min(end=t_kline5min[t_kline5min.__len__() - 1]['timestamp'])
        kline5min.extend(t_kline5min)
    kline5min = kline5min[::-1]
    user = User()
    user.money = 5
    for num in range(121, 1000):
        result = permutation(kline5min[0:num])
        user.refresh_data(kline5min[num - 1])
        if user.can_sell():
            user.calc_total()
        if result == OrderType.多单 and not user.has_order():
            logging.getLogger().info('创建多单')
            user.create_order(kline5min[num - 1]['open'], leverage=50)
        if result == OrderType.空单 and not user.has_order():
            logging.getLogger().info('创建空单')
            user.create_order(kline5min[num - 1]['open'], leverage=50, type=OrderType.空单)


if __name__ == '__main__':
    test()
    # draw_ma()
