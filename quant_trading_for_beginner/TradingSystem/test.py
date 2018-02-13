import pandas_datareader.data as web
#from pandas_datareader import data, wb
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


# class Trade:
#     def __init__(self):
#         self.uuid = uuid.uuid1()
#         self.price = 0
#     def __str__(self):
#         return str(self.uuid) + ' ' + str(self.price)
#     def event_tick(self, price):
#         self.price = price

class Trade:
    def __init__(self, uuid, instrument, entryPrice, stoplossPrice, 
                 profitTargetPrice, commissionrate, commission, 
                 quantity, entryTime, direction):
        self.uuid = uuid
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
        self.event_sendorder = None

    def event_tick(self, market_data):
        pass

    def event_order(self, order):
        pass

    def event_position(self, positions):
        pass



import numpy as np

if __name__ == "__main__":
    data = DataRepository("EURUSD", "D:/GitHub/QuantResearch/quant_trading_for_beginner/data")
    d = data.instance.binsDaily
    print(list(d))
    print(d.loc[d['time'] == 20180102, ' openbid'])

    # print(data.instance.binsH4)
    # print(data.instance.binsM1)
    # trade1 = Trade()
    # print(trade1)

    # trade2 = Trade()
    # print(trade2)
    
    # trade1.event_tick(2)
    # print(trade1)

    # s = Strategy()
    # print(s)

    df1 = pd.DataFrame(np.random.randn(6,4), index=list('abcdef'), columns=list('ABCD'))
    print(df1.loc[['a', 'b', 'd'], 'A'])

    for i in range(1, 3):
        print(i)