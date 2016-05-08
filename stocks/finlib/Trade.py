'''
Created on 7 May 2016

@author: david
'''

class Trade:  
  ID = 0
  
  def __init__(self, buyTime, buyPrice, num=1):
    self.buyPrice    = buyPrice
    self.buyTime     = buyTime
    self.number      = num

    self.sellPrice   = None
    self.sellTime    = None
    
    self.id = Trade.ID ;     Trade.ID +=1
      
  def buyFor(self, invest):
    self.number = int(invest/self.buyPrice)

  def sell(self, time, price):
    self.sellTime   = time
    self.sellPrice  = price

  def costBuy(self):
    return self.number*self.buyPrice

  def costSell(self):
    pass
    
  def gain(self, percent = None):
    pass
  
class TradeLong(Trade):  

  def costSell(self):
    return self.number*self.sellPrice

  def gain(self, percent = None):
    if percent is None:
      return (self.sellPrice-self.buyPrice) * self.number
    else:
      return (self.sellPrice-self.buyPrice) / self.buyPrice * 100
      

class TradeShort(Trade):  

  def costSell(self):
    return self.number*(self.buyPrice + (self.buyPrice-self.sellPrice))

  def gain(self, percent = None):
    if percent is None:
      return -(self.sellPrice-self.buyPrice) * self.number
    else:
      return -(self.sellPrice-self.buyPrice) / self.buyPrice * 100
