'''
Created on 2 May 2016

@author: david
'''
from finlib import TickerData
from Strategies.StrategySTO import StrategySTO

from BackTester import BackTester

import matplotlib.pyplot  as plt
 
ticker = TickerData.TickerData("^FCHI",2016)

print "%s" % ticker.gain()

strategy = StrategySTO(ticker)

tester   = BackTester(ticker, strategy)

tester.run()

slowk = strategy.indicators.get_stoch_slowk()
slowd = strategy.indicators.get_stoch_slowd()

plt.plot(range(slowk.size), slowk, 'r--', range(slowk.size), slowd)

plt.show()