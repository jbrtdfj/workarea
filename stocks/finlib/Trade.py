'''
Created on 7 May 2016

@author: david
'''

class Trade:  
  
  def __init__(self, buyTime, buyPrice, num=1):
    self.buyPrice    = buyPrice
    self.buyTime     = buyTime
    self.number      = num

    self.sellPrice   = None
    self.sellTime    = None
      
  def buyFor(self, invest):
    self.number = int(invest/self.buyPrice)

  def sell(self, time, price):
    self.sellTime   = time
    self.sellPrice  = price

  def cost(self):
    return self.number*self.buyPrice
  
class TradeLong(Trade):  
  pass

class TradeShort(Trade):  
  pass