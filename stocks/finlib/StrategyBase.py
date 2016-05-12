'''
Created on Oct 24, 2010

@author: david
'''
from finlib.TickerIndicators import TickerIndicators
from finlib.Trade import TradeLong, TradeShort

class StrategyBase(object):
  DEBUG = 0
  
  def __init__(self, tickerData, name = ""):
    self.name       = name
    self.data       = tickerData
    self.indicators = TickerIndicators(tickerData);
    
    self.curLongTrade   = []
    self.curShortTrade  = []

    self.doneLongTrade  = []
    self.doneShortTrade = []
    
    self.dateIndex           = -1
    self.capitalBeforeTrade  = 10000
    self.capital             = self.capitalBeforeTrade
  
  def prepare(self):
    self.selectIndicators()

  def initCapital(self, capital):
    self.capitalBeforeTrade  = capital
    self.capital             = self.capitalBeforeTrade

  def runTime(self, dateIndex):
    ''' define the trade to be executed at that date'''
    self.dateIndex           = dateIndex   
    self.indicators.setCurDate(dateIndex)
    
    self.executeTrade()

  
  '''--- EXEC TRADE ---------------------------------'''  
  def executeTrade(self):
    if self.isBuyLongTime():
      trade = TradeLong(self.dateIndex, self.buyLongPrice())
      trade.buyFor(self.capitalBeforeTrade);
      
      self.capital -= trade.costBuy()
      
      self.curLongTrade.append(trade)
      if StrategyBase.DEBUG:
        print "%-5d %2d-LBUY  %4.2f %3.1f %.0f" % (self.dateIndex, trade.id, 
                                              trade.buyPrice, 
                                              self.indicators.value(0, self.dateIndex),
                                              self.totalGain())

    if self.isSellLongTime():
      trade = self.curLongTrade.pop()
      trade.sell(self.dateIndex, self.sellLongPrice())

      self.capital += trade.costSell()

      self.doneLongTrade.append(trade)
      if StrategyBase.DEBUG:
        print "%-5d %2d-LSELL %4.2f %3.1f : %-2.2f%s %.0f" % (self.dateIndex, trade.id, trade.sellPrice, 
                                                  self.indicators.value(0, self.dateIndex), 
                                                  trade.gain(1), "%",
                                                  self.totalGain())
      
    if self.isBuyShortTime():
      trade = TradeShort(self.dateIndex, self.buyShortPrice())
      trade.buyFor(self.capitalBeforeTrade);
      
      self.capital -= trade.costBuy()
      
      self.curShortTrade.append(trade)
      if StrategyBase.DEBUG:
        print "%-5d %2d-SBUY  %4.2f %3.1f" % (self.dateIndex, trade.id, trade.buyPrice, self.indicators.value(0, self.dateIndex))
      
    if self.isSellShortTime():
      trade = self.curShortTrade.pop()
      trade.sell(self.dateIndex, self.sellShortPrice())

      self.capital += trade.costSell()

      self.doneShortTrade.append(trade)
      if StrategyBase.DEBUG:
        print "%-5d %2d-SSELL %4.2f %3.1f : %-2.2f%s" % (self.dateIndex, trade.id, trade.sellPrice, 
                                                  self.indicators.value(0, self.dateIndex), 
                                                  trade.gain(1), "%")
    
  '''--- LONG TRADE ---------------------------------'''  
  def isBuyLongTime(self):
    if self.hasCurrentLongTrade(): return False 
  
    return self.buyLongCondition()

  def buyLongCondition(self):  # !! OVERRIDE !!
    ''' called when no other long trade is on going '''
    return False

  def buyLongPrice(self):  
    return self.data.closePrice(self.dateIndex)

  def isSellLongTime(self):
    if not self.hasCurrentLongTrade(): return False 
  
    return self.sellLongCondition()

  def sellLongCondition(self):   # !! OVERRIDE !!
    ''' called when a long trade is on going '''
    return False

  def sellLongPrice(self):  
    return self.data.closePrice(self.dateIndex)

  '''--- SHORT TRADE ---------------------------------'''  
  def isBuyShortTime(self):
    if self.hasCurrentShortTrade(): return False 
  
    return self.buyShortCondition()

  def buyShortCondition(self):  # !! OVERRIDE !!
    ''' called when no other short trade is on going '''
    return False

  def buyShortPrice(self):  
    return self.data.closePrice(self.dateIndex)

  def isSellShortTime(self):
    if not self.hasCurrentShortTrade(): return False 
  
    return self.sellShortCondition()

  def sellShortCondition(self):   # !! OVERRIDE !!
    ''' called when a long trade is on going '''
    return False

  def sellShortPrice(self):  
    return self.data.closePrice(self.dateIndex)

  '''--- STATUS TRADE ---------------------------------'''  
  def hasCurrentLongTrade(self):
    return len(self.curLongTrade) > 0

  def hasCurrentShortTrade(self):
    return len(self.curShortTrade) > 0
      
  def totalGain(self, percent = None):
    c = self.capital
    
    for t in self.curLongTrade:
      c += t.costBuy()
    
    if percent is None:
      return c
    else:
      return (c / self.capitalBeforeTrade -1)* 100

  def selectIndicators(self):  # !! OVERRIDE !!
    pass

  def get_name(self):        return self.__name
  def set_name(self, value): self.__name = value
  def del_name(self):        del self.__name
  name = property(get_name, set_name, del_name, "name's docstring")
