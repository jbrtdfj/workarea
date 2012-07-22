'''
Created on Oct 6, 2010

@author: david

INVESTMENT RULES:
  stop loss when going below moving average
  when positive, be safe when reaching 3% saving 
  
TO DO
  * analyze low crossing the MA to determine the efficiency of alert 
    + consider the case LOW < MA but CLOSE > MA 
'''
import datetime
import matplotlib.pyplot  as plt
from finance_lib import get_ticker_data_from_web, get_ticker_data_from_file,\
  moving_average

from Strategies.Policies.TradingPolicySimpleMA import TradingPolicySimpleMA,\
  TradingPolicySimpleMAParameter
from Strategies.Brokers.brokers import *
from Strategies.TradeExecuter   import TradeExecuter

r = get_ticker_data_from_web('^FCHI')    
#r = get_ticker_data_from_file('cac40')    
      
prices = r.adj_close
      
""" ---------------- MAIN PROGRAM -------------------- """          

fig = plt.figure()
left, width = 0.1, 0.8
  
def gain_versus_ma(startMA, endMA, stepMA):
  res      = []
  effiency = []
  effiencyWCost = []
  
  maRange = range(startMA, endMA, stepMA)
  
  for ma in maRange:
    policy = TradingPolicySimpleMA(ma, Broker()) 
    exe = TradeExecuter(startDate, policy )
    
    exe.runAll(r)   
    
    ( capitalYield,         annualYield, 
      capitalYieldWCost,    annualYieldWCost, 
      indexYield,           annualIndexYield, 
      tradeEfficiencyWCost, tradeEfficiency,   
      tradeCost )                = exe.getStat(1)
     
    res.append(capitalYieldWCost)
    effiencyWCost.append(tradeEfficiencyWCost)
    effiency.append(tradeEfficiency)
    
  rect1 = [left, 0.55, width, 0.4]
 
  ax = fig.add_axes(rect1)  
  ax.plot(
#           maRange, res,
           maRange, effiency,
           maRange, effiencyWCost
           )

def gain_over_time(ma, doPlot):
  print "## moving average of %i" % ma
  policy = TradingPolicySimpleMA(ma, Broker()) 
  exe = TradeExecuter(startDate, policy )
  
  exe.runAll(r)   
  
  res = (capitalYield,     annualYield, 
   capitalYieldWCost,      annualYieldWCost, 
   indexYield,             annualIndexYield, 
   tradeEfficiencyWCost,   tradeEfficiency,
   tradeCost)        = exe.getStat(1)
  
  print "start time = %i" % exe.initialTradingTime
  print "capitalHistory gain with cost = %.3f, annual yield = %.3f%s (%.2f years)" % (capitalYieldWCost, (annualYieldWCost-1)*100, "%", exe.nbTradeDay/365.0) 
  print "capitalHistory gain           = %.3f, annual yield = %.3f%s (%.2f years)" % (capitalYield, (annualYield-1)*100, "%", exe.nbTradeDay/365.0) 
  print "index   gain                  = %.3f, annual yield = %.3f%s (%.2f years)" % (indexYield, (annualIndexYield-1)*100, "%", exe.nbTradeDay/365.0) 
  print "EFFICIENCY = %.3f" % (tradeEfficiencyWCost)
  print "number of trade  = %i over %i trading day (%.2f%s), ie every %.2f days" % \
                    (exe.nbTrade, exe.nbTradeDay, float(exe.nbTrade)/exe.nbTradeDay*100, "%", exe.nbTradeDay/exe.nbTrade)
  print "total trade cost = %.2f" % (tradeCost)
       
  if doPlot:     
#   rect2 = [left, 0.1, width, 0.4]
#   ax2 = fig.add_axes(rect2) 
    plt.plot(
           range(len(prices[exe.initialTradingTime:])), prices[exe.initialTradingTime:],
           range(len(policy.maLarge[exe.initialTradingTime:])), policy.maLarge[exe.initialTradingTime:],
  #         range(len(ma10[initialTradingTime:])), ma10[initialTradingTime:],
           range(len(exe.capitalHistory)), exe.capitalHistory,
           range(len(exe.tradeStatus)), exe.tradeStatus,
           )
    
  return [res, exe.nbTrade, exe.nbTradeDay]
  
startDate = datetime.date(2005,1,1)
  
doPlot = True
TradingPolicySimpleMAParameter.enableGainSavingOnInvest = False
TradingPolicySimpleMAParameter.dumpTrace                = False
TradingPolicySimpleMAParameter.useAlertBelowMACross     = True
TradingPolicySimpleMAParameter.InvestLowBelowMAMargin   = 1 
gain_over_time(100, doPlot)
#gain_versus_ma(2, 200, 2)
 
#"""**** Low cross MA """
#TradingPolicySimpleMAParameter.useAlertBelowMACross = True
#for i in range(0, 1, 1):
#  print "-------- %f " % (i/2.0)
#  TradingPolicySimpleMAParameter.InvestLowBelowMAMargin = 1 - 0.005*i
#    
#  gain_over_time(100, False)

if doPlot:
  plt.show()