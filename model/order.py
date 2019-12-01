import logging
from enum import Enum


class OrderType(Enum):
    多单 = 1
    空单 = 0


class Order:
    open = 0.0
    current = 0.0
    qty = 0.0
    leverage = 0.0
    pnl_ratio = 0.0
    # 0 多， 1 空
    type = 0.0

    def __init__(self, open, qty, leverage, type=OrderType.多单):
        self.open = open
        self.current = open
        self.qty = qty * leverage
        self.leverage = leverage
        self.type = type

    def refresh_data(self, kline):
        self.current = kline['close']
        result = self.current - self.open
        if self.type == OrderType.空单:
            result = 0 - result
        self.pnl_ratio = ((result / self.open) * 100.0) * 50.0
        logging.getLogger().info('刷新订单数据, 当前价格：%s, 开仓价格：%s 开仓数量：%s 利率： %s', self.current, self.open, self.qty, self.pnl_ratio)

    def get_money(self):
        return self.qty / self.leverage + (self.qty / self.leverage) * (self.pnl_ratio / 100.0)
