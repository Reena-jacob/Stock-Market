#!/usr/bin/python3

import math
import decimal

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

class StockType(Enum):
    Common = 1
    Preferred = 2

class Indicator(Enum):
    BUY = 1
    SELL = 2

@dataclass
class Trade:
    timestamp: datetime
    quantity: int
    indicator: Indicator
    price: float

class Stock:
    def __init__(self, stock_type, par_value, fixed_dividend=0):
        self.stock_type = stock_type
        self.par_value = par_value
        self.fixed_dividend = fixed_dividend
        self.dividend_history = []

    def distribute_dividend(self, dividend_amount=0):
        if self.stock_type == StockType.Preferred:
            dividend_amount = self.fixed_dividend * self.par_value

        self.dividend_history.append(dividend_amount)

    def dividend_yield(self, price):
        last_dividend = 0
        if self.dividend_history:
            last_dividend = self.dividend_history[-1]
        return last_dividend/price
    
    def P_E_ratio(self, price):
        if not self.dividend_history:
            print('P/E Ratio cannot be calculated')
            return
        last_dividend = self.dividend_history[-1]
        if last_dividend == 0:
            print('P/E Ratio cannot be calculated')

        return price/last_dividend

class StockMarket:
    def __init__(self):
        self.trade_history = {}
        self.stocks = {}

    def add_stock(self, symbol, stock):
        self.stocks[symbol] = stock

    def record_trade(self, symbol, timestamp, quantity, indicator, price):
        trade = Trade(timestamp=timestamp, quantity=quantity, indicator=indicator, price=price)
        if symbol not in self.trade_history:
            self.trade_history[symbol] = []
        self.trade_history[symbol].append(trade)

    def VWSP(self, symbol, timespan=timedelta(minutes=5)):
        vwsp = 0
        now = datetime.now()
        quantity_sum = 0
        price_quantity_sum = 0
        for trade in self.trade_history[symbol]:
            if now - trade.timestamp > timespan:
                continue
            quantity_sum = quantity_sum + trade.quantity
            price_quantity_sum = price_quantity_sum + (trade.price * trade.quantity)

        if quantity_sum:
            vwsp = price_quantity_sum / quantity_sum
        return vwsp

    def GBCE_ASI(self):
        stock_vwsp = []
        for symbol in self.stocks.keys():
            stock_vwsp.append(self.VWSP(symbol))

        return math.exp(math.fsum(math.log(vwsp) for vwsp in stock_vwsp) / len(stock_vwsp))


if __name__ == '__main__':
    market = StockMarket()
    TEA = Stock(StockType.Common, 100)
    market.add_stock('TEA', TEA)
    POP = Stock(StockType.Common, 100)
    market.add_stock('POP', POP)
    ALE = Stock(StockType.Common, 60)
    market.add_stock('ALE', ALE)
    GIN = Stock(StockType.Preferred, 100, fixed_dividend=2)
    market.add_stock('GIN', GIN)
    JOE = Stock(StockType.Preferred, 250)
    market.add_stock('JOE', JOE)
    TEA.distribute_dividend(0)
    POP.distribute_dividend(8)
    ALE.distribute_dividend(23)
    GIN.distribute_dividend()
    JOE.distribute_dividend(13)
    print(ALE.dividend_yield(price=314))
    print(GIN.P_E_ratio(price=839))

    market.record_trade('TEA', datetime.now(), 200, Indicator.BUY, 435)
