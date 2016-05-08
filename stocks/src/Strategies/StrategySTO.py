'''
Created on 8 May 2016

@author: david
'''
from finlib.StrategyBase import StrategyBase
from finlib.TickerIndicators import TickerIndicators

class StrategySTO(StrategyBase):
  LIM_LOW  = 20   ; LIM_HIGH  = 80
  SLIM_LOW = 20   ; SLIM_HIGH = 85
  CROSS_UP = "UP" ; CROSS_DOWN = "DN";
  
  def __init__(self, tickerData, name = ""):
    super(StrategySTO,self).__init__(tickerData, name)

    self.LS_USE_MAX_HIGH = False
    self.LS_USE_MAX_MED  = False
    self.LB_USE_CROSS    = StrategySTO.CROSS_DOWN
    
    self.SB_USE_CROSS   = StrategySTO.CROSS_UP
    self.SS_USE_MAX_LOW = False
    self.SS_USE_MAX_MED  = False
  
  def selectIndicators(self):
    ''' define which indicator are used for the trading '''
    self.indicators.activate(TickerIndicators.STO_LOW_K)
    self.indicators.activate(TickerIndicators.STO_LOW_D)
    
  def buyLongCondition(self):
    ''' called when no other long trade on going '''
    if self.LB_USE_CROSS == StrategySTO.CROSS_DOWN:
      return self.indicators.lessThan(0, StrategySTO.LIM_LOW)
    else:
      return self.indicators.crossUp(0, StrategySTO.LIM_LOW)

  def sellLongCondition(self):
    ''' called when a long trade on going '''
    if self.indicators.greaterThan(0, StrategySTO.LIM_HIGH) : 
      if self.LS_USE_MAX_HIGH: return self.indicators.max(1)
      return True
              
    if self.LS_USE_MAX_MED and self.indicators.max(1): return True
    
    return False

  def buyShortCondition(self):
    ''' called when no other long trade on going '''
    if self.SB_USE_CROSS == StrategySTO.CROSS_UP:
      return self.indicators.greaterThan(0, StrategySTO.SLIM_HIGH)
    else:
      return self.indicators.crossDown(0, StrategySTO.SLIM_HIGH)
           
  def sellShortCondition(self):
    ''' called when a short trade on going '''
    if self.indicators.lessThan(0, StrategySTO.SLIM_LOW) : 
      if self.SS_USE_MAX_LOW: return self.indicators.min(1)
      return True
              
    if self.SS_USE_MAX_MED and self.indicators.min(1): return True
    
    return False
      
