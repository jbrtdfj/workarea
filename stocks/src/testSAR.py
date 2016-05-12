'''
Created on 2 May 2016

@author: david
'''
from finlib import TickerData
from finlib.StrategyBase import StrategyBase
from finlib.TickerIndicators import  TickerIndicators
from Strategies.StrategySAR import StrategySAR

from finlib.BackTester import BackTester

import matplotlib.pyplot  as plt

tickerName =  "^FCHI"

StrategyBase.DEBUG = 1
y = 2013

ticker = TickerData.TickerData(tickerName,y)

s = StrategySAR(ticker, "%s" % (y))

tester   = BackTester(ticker, s)
  
tester.run()

ind = TickerIndicators(ticker)
sar = ind.get_sarmclose()

plt.plot(range(sar.size), sar+ticker.close(), 'r--',range(ticker.close().size), ticker.close())

plt.show()