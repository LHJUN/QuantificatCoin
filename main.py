import numpy
from pyecharts.charts import Line
from pyecharts.options import DataZoomOpts, AxisOpts, TitleOpts

from calc.coinData import KlineApi, MAApi, permutation
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def draw_ma():
    kline_1day = KlineApi.get_kline_5min()[::-1]
    times = list(map(lambda x: x['timestamp'], kline_1day))[120:]
    closes = numpy.array(list(map(lambda x: x['close'], kline_1day)))
    ma30data = list(map(lambda x: round(x, 3), MAApi.getMa30(numpy.array(closes)).tolist()))[120:]
    ma60data = list(map(lambda x: round(x, 3), MAApi.getMa60(numpy.array(closes)).tolist()))[120:]
    ma120data = list(map(lambda x: round(x, 3), MAApi.getMa120(numpy.array(closes)).tolist()))[120:]
    c = (
        Line()
            .add_xaxis(times)
            .add_yaxis("MA30", ma30data, is_smooth=True)
            .add_yaxis("MA60", ma60data, is_smooth=True)
            .add_yaxis("MA120", ma120data, is_smooth=True)
            .set_global_opts(
            datazoom_opts=DataZoomOpts(is_show=True, type_='inside'),
            xaxis_opts=AxisOpts(is_scale=True),
            title_opts=TitleOpts(title="Line-smooth")
        )
    )
    logging.getLogger().info(c.render())


def test():
    flag = 0
    kline5min = KlineApi.get_kline_5min()
    for num in range(121, 299):
        result = permutation(kline5min[0:num])
        if result == 'create_order' and flag == 0:
            print('create_order')
            flag = 1
        if result == 'sell_order' and flag == 1:
            print('sell_order')
            flag = 0


if __name__ == '__main__':
    draw_ma()
