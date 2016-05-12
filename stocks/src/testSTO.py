'''
Created on 2 May 2016

@author: david
'''
from finlib import TickerData
from finlib.StrategyBase import StrategyBase
from finlib.TickerIndicators import  TickerIndicators
from Strategies.StrategySTO import StrategySTO

from finlib.BackTester import BackTester

import matplotlib.pyplot  as plt

tickerName =  "^FCHI"

StrategyBase.DEBUG = 1
y = 2015

for year in range(y, y+1):
  ticker = TickerData.TickerData(tickerName,year, start=[2014,6,1])

  print "%4d %s TOTAL GAIN : %2.1f%s------------" % (year, tickerName, ticker.gain()[2], '%')

  for cross in [StrategySTO.CROSS_DOWN]:
    for use_max_med in [False]:
      
      for use_max_high in [False]:
        s = StrategySTO(ticker, '%-10s-%s-%s' % ('MED_MAX' if use_max_med  else 'MED_NO_MAX',
                                                 'HIG_MAX' if use_max_high else 'HIG_NO_MAX',
                                                 cross))
    
        s.LB_USE_CROSS    = cross
        s.LS_USE_MAX_MED  = use_max_med
        s.LS_USE_MAX_HIGH = use_max_high
    
        tester   = BackTester(ticker, s)
  
        tester.run()

ind = TickerIndicators(ticker)
slowk = ind.get_stoch_slowk()
slowd = ind.get_stoch_slowd()

plt.plot(range(slowk.size), slowk, 'r--', range(slowk.size), slowd)

plt.show()