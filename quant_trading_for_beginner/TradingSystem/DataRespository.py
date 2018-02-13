"""
README
======
This file contains Python codes.
======
"""

""" Implementing a Backtesting System """

""" Store a single unit of data """

class TickData:
    def __init__(self, symbol, openTime, closeTime, 
                openBid, highBid, lowBid, closeBid,
                openAsk, highAsk, lowAsk, closeAsk,
                volume, pnl, length):
        self.symbol = symbol
        self.openTime = openTime
        self.closeTime = closeTime
        self.openBid = openBid
        self.highBid = highBid
        self.lowBid = lowBid
        self.closeBid = closeBid
        self.openAsk = openAsk
        self.highAsk = highAsk
        self.lowAsk = lowAsk
        self.closeAsk = closeAsk
        self.volume = volume
        self.pnl = pnl
        self.length = length

import pandas as pd
import uuid

class DataRepository:
    class __DataResopistory:
        def __init__(self, ticker, data_path):
            self.ticker = ticker
            self.data_path = data_path
            self.binsDaily = pd.read_csv(data_path + '/' + ticker + '_D1')
            self.binsH4 = pd.read_csv(data_path + '/' + ticker + '_H4')
            self.binsM1 = pd.read_csv(data_path + '/' + ticker + '_M1')
        def __str__(self):
            return self.data_path + '/' + self.ticker
    instance  = None
    def __init__(self, ticker, data_path):
        if not DataRepository.instance:
            DataRepository.instance = DataRepository.__DataResopistory(ticker, data_path)

class Trade:
    def __init__(self, instrument, entryPrice, stoplossPrice, 
                 profitTargetPrice, commissionrate, commission, 
                 quantity, entryTime, direction):
        self.uuid = uuid.uuid1()
        self.instrument = instrument
        self.entryPrice = entryPrice
        self.exitPrice = 0
        self.stoplossPrice = stoplossPrice
        self.profitTargetPrice = profitTargetPrice
        self.commissionrate = commissionrate
        self.commission = commission
        self.profit = 0
        self.quantity = quantity
        self.entryTime = entryTime
        self.exitTime = 0
        self.direction = direction

    def close_trade(self, exitPrice, exitTime):
        self.exitPrice = exitPrice
        self.exitTime = exitTime
        self.profit = self.calc_profit(exitPrice)

    def calc_profit(self, price):
        return self.quantity * (price - self.entryPrice - self.commission)

""" Base strategy for implementation """
class Strategy:
    def __init__(self):
        self.strategy_name = None

    def event_tick(self, market_data):
        pass

    def event_order(self, order):
        pass

    def event_position(self, positions):
        pass

class TestStrategy(Strategy):
    def __init__(self, symbol):
        Strategy.__init__(self)
        self.symbol = symbol
        self.trades = dict()

    def runSimulation(self, binsDaily, binsM1):
        prevBin2 = None
        for day in binsDaily['Time']:
            long_limit = binsDaily.loc[binsDaily['Time'] == day, 'lowAsk']
            short_limit = binsDaily.loc[binsDaily['Time'] == day, 'highAsk']
            dayBinsM1 = binsM1.loc[binsM1['Time'].date() == day]
            for i in range(dayBinsM1.shape[0]):
                bin1 = dayBinsM1.loc[i]
                if i == 0:
                    bin2 = prevBin2
                else:
                    bin2 = dayBinsM1.loc[i - 1]
                if bin2 is not None:
                    if bin1['lowAsk'] <= long_limit and bin2['closeAsk'] > long_limit:
                        trade = Trade('FX', bin1['lowAsk'], 
                        bin1['lowAsk'] * 0.8, bin1['lowAsk'] * 1.2, 0.1, 6.5, 
                        100, bin1['Time'], 'long')
                        self.trades[str(trade.uuid)] = trade
                if bin2 is not None:
                    if bin1['highBid'] >= short_limit and bin2['closeBid'] < short_limit:
                        trade = Trade('FX', bin1['highBid'], 
                        bin1['highBid'] * 0.8, bin1['highBid'] * 1.2, 0.1, 6.5, 
                        100, bin1['Time'], 'short')
                        self.trades[str(trade.uuid)] = trade
            prevBin2 = dayBinsM1.loc[-1]
        for 
            
import datetime as dt
import pandas as pd

class Backtester:
    def __init__(self, symbol, start_date, end_date,
                 data_source="google"):
        self.target_symbol = symbol
        self.data_source = data_source
        self.start_dt = start_date
        self.end_dt = end_date
        self.strategy = None
        self.unfilled_orders = []
        self.positions = dict()
        self.current_prices = None
        self.rpnl, self.upnl = pd.DataFrame(), pd.DataFrame()

    def get_timestamp(self):
        return self.current_prices.get_timestamp(
            self.target_symbol)

    def get_trade_date(self):
        timestamp = self.get_timestamp()
        return timestamp.strftime("%Y-%m-%d")

    def update_filled_position(self, symbol, qty, is_buy,
                               price, timestamp):
        position = self.get_position(symbol)
        position.event_fill(timestamp, is_buy, qty, price)
        self.strategy.event_position(self.positions)
        self.rpnl.loc[timestamp, "rpnl"] = position.realized_pnl

        print(self.get_trade_date(), \
            "Filled:", "BUY" if is_buy else "SELL", \
            qty, symbol, "at", price)

    def get_position(self, symbol):
        if symbol not in self.positions:
            position = Position()
            position.symbol = symbol
            self.positions[symbol] = position

        return self.positions[symbol]

    def evthandler_order(self, order):
        self.unfilled_orders.append(order)

        print(self.get_trade_date(), \
            "Received order:", \
            "BUY" if order.is_buy else "SELL", order.qty, \
             order.symbol)

    def match_order_book(self, prices):
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = \
                [order for order in self.unfilled_orders
                 if self.is_order_unmatched(order, prices)]

    def is_order_unmatched(self, order, prices):
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)

        if order.is_market_order and timestamp > order.timestamp:
            # Order is matched and filled.
            order.is_filled = True
            open_price = prices.get_open_price(symbol)
            order.filled_timestamp = timestamp
            order.filled_price = open_price
            self.update_filled_position(symbol,
                                        order.qty,
                                        order.is_buy,
                                        open_price,
                                        timestamp)
            self.strategy.event_order(order)
            return False

        return True

    def print_position_status(self, symbol, prices):
        if symbol in self.positions:
            position = self.positions[symbol]
            close_price = prices.get_last_price(symbol)
            position.update_unrealized_pnl(close_price)
            self.upnl.loc[self.get_timestamp(), "upnl"] = \
                position.unrealized_pnl

            print(self.get_trade_date(), \
                "Net:", position.net, \
                "Value:", position.position_value, \
                "UPnL:", position.unrealized_pnl, \
                "RPnL:", position.realized_pnl)

    def evthandler_tick(self, prices):
        self.current_prices = prices
        self.strategy.event_tick(prices)
        self.match_order_book(prices)
        self.print_position_status(self.target_symbol, prices)

    def start_backtest(self):
        self.strategy = MeanRevertingStrategy(self.target_symbol)
        self.strategy.event_sendorder = self.evthandler_order

        mds = MarketDataSource()
        mds.event_tick = self.evthandler_tick
        mds.ticker = self.target_symbol
        mds.source = self.data_source
        mds.start, mds.end = self.start_dt, self.end_dt

        print("Backtesting started...")
        mds.start_market_simulation()
        print("Completed.")


if __name__ == "__main__":
    backtester = Backtester("AAPL",
                            dt.datetime(2014, 1, 1),
                            dt.datetime(2014, 12, 31))
    backtester.start_backtest()

    import matplotlib.pyplot as plt
    backtester.rpnl.plot()
    plt.show()

    backtester.upnl.plot()
    plt.show()