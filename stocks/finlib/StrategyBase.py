'''
Created on Oct 24, 2010

@author: david
'''
from finlib.TickerIndicators import TickerIndicators
from finlib.Trade import TradeLong

class StrategyBase(object):

  def __init__(self, tickerData):
    self.data       = tickerData
    self.indicators = TickerIndicators(tickerData);
    
    self.usedIndicators = []
    self.curLongTrade   = []
    self.curShortTrade  = []

    self.doneLongTrade  = []
    self.doneShortTrade = []
    
    self.dateIndex           = -1
    self.capitalBeforeTrade  = 10000
    self.capital             = self.capitalBeforeTrade
  
  def runTime(self, dateIndex):
    ''' define the trade to be executed at that date'''
    self.dateIndex           = dateIndex   

    self.prepareData()
    self.executeTrade()

  def initCapital(self, capital):
    self.capitalBeforeTrade  = capital
    self.capital             = self.capitalBeforeTrade

  def prepareData(self):
    pass
  
  '''--- EXEC TRADE ---------------------------------'''  
  def executeTrade(self):
    if self.isBuyLongTime():
      trade = TradeLong(self.dateIndex, self.data.closePrice(self.dateIndex))
      trade.buyFor(self.capitalBeforeTrade);
      
      self.capital -= trade.cost()
      
      self.curLongTrade.append(trade)
      print "%-5d BUY %f" % (self.dateIndex, self.indValue(0))
     
  '''--- LONG TRADE ---------------------------------'''  
  def isBuyLongTime(self):
    if self.hasCurrentLongTrade(): return False 
  
    return self.buyLongCondition()

  def buyLongCondition(self):
    ''' called when no other long trade is on going '''
    return False

  def isSellLongTime(self):
    if not self.hasCurrentLongTrade(): return False 
  
    return self.sellLongCondition()

  def sellLongCondition(self):
    ''' called when no other long trade is on going '''
    return False

  '''--- SHORT TRADE ---------------------------------'''  
  def isBuyShortTime(self):
    return False

  def isSellShortTime(self):
    return False

  '''--- INDICATORS API ---------------------------------'''  
  def indValue(self, indIndex):
    return self.usedIndicators[0][self.dateIndex]

  def indGreater(self, indIndex, limit):
    return self.usedIndicators[0][self.dateIndex] > limit

  def indLessThan(self, indIndex, limit):
    return self.usedIndicators[0][self.dateIndex] < limit

  def indCrossUp(self, indIndex, limit):
    now = self.usedIndicators[0][self.dateIndex]
    z1  = self.usedIndicators[0][self.dateIndex-1]
    
    return (now > limit and z1 < limit)

  '''--- STATUS TRADE ---------------------------------'''  
  def hasCurrentLongTrade(self):
    return len(self.curLongTrade) > 0

  def hasCurrentShortTrade(self):
    return self.curShortTrade.size > 0
      
  def spentCapital(self):
    ''' capital spend at the current time '''
    return 0
