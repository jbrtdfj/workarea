'''
Created on 8 May 2016

@author: david
'''
from finlib.StrategyBase import StrategyBase
from finlib.TickerIndicators import TickerIndicators

class StrategySAR(StrategyBase):
  
  def __init__(self, tickerData, name = ""):
    super(StrategySAR,self).__init__(tickerData, name)

  
  def selectIndicators(self):
    ''' define which indicator are used for the trading '''
    self.indicators.activate(TickerIndicators.SARmCLOSE)
    self.indicators.activate(TickerIndicators.SAR)
    
  def buyLongCondition(self):
    ''' called when no other long trade on going '''
    return self.indicators.crossDown(0,0)

  def buyLongPrice(self):  
    return self.indicators.value(1, self.dateIndex-1)

  def sellLongCondition(self):
    ''' called when a long trade on going '''
    return self.indicators.crossUp(0,0)

  def sellLongPrice(self):  
    return self.buyLongPrice()

  def buyShortCondition(self):
    ''' called when no other long trade on going '''
    return self.indicators.crossUp(0,0)

  def buyShortPrice(self):  
    return self.indicators.value(1, self.dateIndex-1)
           
  def sellShortCondition(self):
    ''' called when a short trade on going '''
    return self.indicators.crossDown(0,0)

  def sellShortPrice(self):  
    return self.indicators.value(1, self.dateIndex-1)
      
