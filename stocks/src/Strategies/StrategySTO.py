'''
Created on 8 May 2016

@author: david
'''
from finlib.StrategyBase import StrategyBase

class StrategySTO(StrategyBase):
  LIM_LOW  = 20
  LIM_HIGH = 80
  
  def __init__(self, tickerData):
    super(StrategySTO,self).__init__(tickerData)

  def prepareData(self):
    ''' define the trade to be executed at that date'''
    
    self.usedIndicators.append(self.indicators.get_stoch_slowk())
    
    
  def buyLongCondition(self):
    ''' called when no other long trade on going '''
    return self.indCrossUp(0,  StrategySTO.LIM_LOW)
  
  def sellLongCondition(self):
    ''' called when no other long trade on going '''
    return self.sto > StrategySTO.LIM_HIGH

           
      
