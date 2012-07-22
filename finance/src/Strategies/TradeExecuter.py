'''
Created on Oct 24, 2010

@author: david
'''
import datetime
from Strategies.Policies.TradingPolicySimpleMA import TradingPolicySimpleMAParameter

flagInvest = 1
flagHold   = 0

class TradeExecuter:
  movavgLarge          = 10
  startAnalysisDate    = None
  nbTrade              = 0
  nbTradeDay           = 0
  tradeStatus          = [flagHold]
  initialTradingTime   = -1
  initialTradingTime   = 0;
  capitalHistory       = []
  tradeCosts           = [0]

  """ INTERNAL """
  # policy
  dates         = []
  pricesClose   = []
  state         = 'hold' # 'invest'
  capital       = 0
  investStarted = 0
  
  def __init__(self, startTradeDate, policy):
    self.startAnalysisDate = startTradeDate
    self.policy            = policy
  
  def runAll(self, tickerRecords): 
    self.dates                = tickerRecords.date
    self.pricesClose          = tickerRecords.adj_close 
    self.policy.tickerRecords = tickerRecords
      
    if (TradingPolicySimpleMAParameter.dumpTrace): 
      print "type temps close low ma holdprice cur_capital state -> new_state capital"
                
    # find initial trade day/time
    startFound = False
    for t in range(1, len(self.pricesClose)):
      if not startFound:
        self.initialTradingTime = t
        self.capital            = self.pricesClose[t]
        self.capitalHistory     = [ self.capital ]
          
        if self.dates[t] >= self.startAnalysisDate:
          startFound = True

      if startFound:
        self.run(t)

    minIndex = self.pricesClose[self.initialTradingTime:].min()
    maxIndex = self.pricesClose[self.initialTradingTime:].max()
    self.tradeStatus = [minIndex if x == flagHold else maxIndex for x in self.tradeStatus]

  def run(self, t):
    self.nbTradeDay += 1
    
    (self.state, self.capital, tradeCost) = self.policy.run(self.state, t, self.capital);

    # detect first investment
    if self.investStarted == 0 and self.state == 'invest':
      self.capital        = self.pricesClose[t]
      self.capitalHistory = [self.capital for x in self.capitalHistory]
      self.tradeCosts     = [0 for x in self.capitalHistory]
      self.investStarted  = 1

    self.capitalHistory.append(self.capital)
    self.tradeCosts.append(tradeCost)
    
    self.nbTrade += self.policy.nbTrade
          
    self.tradeStatus.append(flagInvest if self.state == 'invest' else flagHold)      
      
  def getStat(self, numShares):
    
    tradeCost = sum(self.tradeCosts)
    
    capitalYield = self.capitalHistory[-1]/self.capitalHistory[0]
    annualYield  = pow(capitalYield, 1./(self.nbTradeDay/365.0))

    capitalYieldWCost = (self.capitalHistory[-1] / self.capitalHistory[0] * 10000 - tradeCost) / 10000 # self.capitalHistory[0]
    annualYieldWCost  = pow(capitalYieldWCost, 1./(self.nbTradeDay/365.0))

    indexYield        = self.pricesClose[-1]/self.pricesClose[self.initialTradingTime]
    annualIndexYield  = pow(indexYield, 1./(self.nbTradeDay/365.0))
    
    tradeEfficiencyWCost = capitalYieldWCost / indexYield

    tradeEfficiency      = capitalYield / indexYield
    
    return (capitalYield,      annualYield,
            capitalYieldWCost, annualYieldWCost, 
            indexYield,        annualIndexYield, tradeEfficiencyWCost, tradeEfficiency, tradeCost)
