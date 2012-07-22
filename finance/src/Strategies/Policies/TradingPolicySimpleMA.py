'''
Created on Oct 24, 2010

@author: david
'''
from finance_lib import moving_average

class Trade:
  time        = 0
  buyPrice    = 0
  maxPrice    = 0
  holdPrice   = None
  holdReached = False
  
  def __init__(self, time, buyPrice):
    self.time      = time
    self.buyPrice  = buyPrice
    self.maxPrice  = buyPrice
    self.holdPrice = None
  
  def setCurrentPrice(self, price):
    if price > self.maxPrice: self.maxPrice = price

class TradingPolicySimpleMAParameter:
  dumpTrace                = False  # True

  maDelay                  = 1      # seems to be the optimal value

  enableGainSavingOnInvest = True
  savingGain               = 1.03
  
  # Down crossing MA when in invest state
  useAlertBelowMACross     = True
  useInvestLowVersusMA     = True
  InvestLowBelowMAMargin   = 1 - 0.01  # 
  
class TradingPolicySimpleMA:
  nbTrade     = 0
      
  """ INTERNAL VARIABLE """
  maLarge            = []
  pricesClose        = []
  pricesLow          = []
  tickerRecords      = None
  broker             = None
  movavgLarge        = 100
  maLarge_value      = 0
  priceClose         = 0
  gain               = 0
  trade              = None
  
  def __init__(self, movavgLarge, broker = None):
    self.movavgLarge = movavgLarge
    self.broker      = broker
    
  def __setattr__(self, name, value):
    if (name == "tickerRecords"):
      self.__dict__["pricesClose"]        = value.adj_close
      self.__dict__["pricesLow"]          = value.low
      self.maLarge = moving_average(value.adj_close, self.movavgLarge, type='simple')
    else:
      self.__dict__[name] = value
      
  def run(self, state, t, curCapital):
    """ return newState, newCapital, tradeCost """
    self.maLarge_value      = self.maLarge[t - TradingPolicySimpleMAParameter.maDelay] 
    self.priceClose         = self.pricesClose[t]
    self.priceLow           = self.pricesLow[t]
    self.nbTrade            = 0
    
    if (state == 'hold'):
      res = self.runHoldState(t, curCapital)
      
    elif (state == 'invest'):
      res = self.runInvestState(t, curCapital)

    elif (state == 'investonhold'):
      res = self.runInvestOnHoldState(t, curCapital)
  
    if self.trade != None:
      self.trade.setCurrentPrice(self.priceClose)
       
    self.updateHoldPrice(self.priceClose)
     
    if (TradingPolicySimpleMAParameter.dumpTrace): 
      print "trade %i %10.2f %10.2f %10.2f %10.2f %10.2f %10s -> %10s %10.2f" % \
               (t, self.priceClose, self.priceLow, self.maLarge_value, 
                self.trade.holdPrice * (1 if self.trade.holdReached else -1), 
                curCapital, state, res[0], res[1])    
    return res
    
  def runInvestState(self, t, curCapital):
    newCapital = curCapital
    tradeCost  = 0    

    prevPrice = self.pricesClose[t-1]
    
    for res in self.shouldSellOnInvest(t):
      (tradeType, tradePrice, newState) = res
      
      if tradeType == 'sell':
        self.nbTrade += 1
        newCapital *= (tradePrice / prevPrice) 
        if (self.broker != None):
          tradeCost += self.broker.tradeCost(newCapital)
      elif tradeType == 'buy':
        self.nbTrade += 1
        if (self.broker != None):
          tradeCost += self.broker.tradeCost(newCapital)
      else:
        # remain in invest state, adjust capital
        newCapital *= (tradePrice / prevPrice)

      prevPrice = tradePrice
      
    return (newState, newCapital, tradeCost)

  def shouldSellOnInvest(self, t): 
    res = []
    
    if TradingPolicySimpleMAParameter.enableGainSavingOnInvest and \
          self.trade.holdReached and self.priceClose < self.trade.holdPrice:
        res.append( ('sell', self.trade.holdPrice, 'investonhold') )

    elif TradingPolicySimpleMAParameter.useAlertBelowMACross:
      maThr = self.maLarge_value * TradingPolicySimpleMAParameter.InvestLowBelowMAMargin
      
      if self.priceLow < maThr :
        # low below ma + margin
        if TradingPolicySimpleMAParameter.dumpTrace:
          print "low_crossing %.2f %.2f %.2f %s" % (self.priceLow, maThr, self.priceClose, \
                  "!!!" if self.priceClose > maThr else "")
        
        res.append(('sell',  maThr, 'hold'))

        if self.priceClose > self.maLarge_value:
          res.append(('buy',  self.priceClose, 'invest'))
          
      elif self.priceClose < self.maLarge_value:
        res.append( ('sell', self.priceClose, 'hold') )
        
    elif self.priceClose < self.maLarge_value:
      res.append( ('sell', self.priceClose, 'hold') )
            
    if len(res) == 0:
      # remain in invest state
      res.append( ('none', self.pricesClose[t], 'invest') )
      
    return res

  def updateHoldPrice(self, price):
    if (self.trade.holdPrice == None):
      self.trade.holdPrice = price * TradingPolicySimpleMAParameter.savingGain
      
    elif self.trade.holdReached == False:
      if price > self.trade.holdPrice:
        self.trade.holdReached = True

  def runInvestOnHoldState(self, t, curCapital):
    newState = 'investonhold'
     
    if self.priceClose >  self.trade.holdPrice:
      newState = 'invest'
       
    elif self.priceClose <= self.maLarge_value:
      newState = 'hold'
      
    return ( newState, curCapital, 0)
  
  def runHoldState(self, t, curCapital):
    #    newCapital *= (1/gain)
    newCapital = curCapital  
    newState   = 'hold'
    tradeCost  = 0    
    
    if self.priceClose > self.maLarge_value:
      newState = 'invest'
      self.nbTrade += 1
      if (self.broker != None):
        tradeCost += self.broker.tradeCost(newCapital)

    self.trade = Trade(t, self.priceClose)
    
    return (newState, newCapital, tradeCost)
