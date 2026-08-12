from ib_async import IB
from ib_async import Stock
ib = IB()

ib.connect('127.0.0.1', 4002, 16)
ib.reqMarketDataType(3)

contract = Stock('AAPL', 'SMART', 'USD')
data = ib.reqHistoricalData(contract, '', '3 D', '15 mins', 'TRADES', False)

print(data)