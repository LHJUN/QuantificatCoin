import logging
from enum import Enum

from model.order import Order, OrderType


class User:
    money = 0
    order = None

    def refresh_data(self, kline):
        if self.has_order():
            self.order.refresh_data(kline)
            money_ = self.money + self.order.get_money()
            logging.getLogger().info('还剩…%s', money_)
            return money_

    def calc_total(self):
        self.money = self.money + self.order.get_money()
        self.order = None
        logging.getLogger().info('卖出结算…%s', self.money)

    def create_order(self, open, leverage, type=OrderType.多单):
        self.order = Order(open=open, qty=self.money / 5.0, leverage=leverage, type=type)
        self.money = self.money - self.money / 5.0

    def has_order(self):
        return self.order is not None

    def can_sell(self):
        return self.has_order() and (self.order.pnl_ratio < - 20.0 or self.order.pnl_ratio > 50.0)
