'''
Created on Oct 6, 2010

@author: david

INVESTMENT RULES:
  invest in the best stock after N months
'''
import datetime
from finance_lib import get_ticker_data_from_web_stend
import math

tickers = {'AC':0,  'ALO':2005, 'AI':0,  'ALU':0, 'CS':0,  'BNP':0, 'EN':0,
           'CA':0,  'ACA':0,    'BN':0,  'EAD':0, 'EI':0,
           'FTE':0, 'GSZ':0,    'LG':0,  'OR':0,  'MC':0,  'ML':0,  'KN':0,     'RI':0,     'UG':0,
           'PP':0,  'PUB':0,    'RNO':0, 'SGO':0, 'SAN':0, 'SU':0,  'GLE':0,    'STM':0,
           'TEC':0, 'FP':0,     'UL':0,  'VIE':0, 'DG':0,  'VIE':0, 'EDF':2006, 
           'SEV':2009, 'VK':2011, 'MT':2011, 'CAP':2011 }
      
def compute_performance(year):
  results = {}

  start = datetime.date(year,1,1)
  end = datetime.date(year+1,1,1)

  
  r = get_ticker_data_from_web_stend('^FCHI', start, end)    
  pricesCAC = r.close
  ratioCACInit = (pricesCAC[decisionTime]/pricesCAC[0]-1)*100
  ratioCAC     = (pricesCAC[-1]/pricesCAC[0]-1)*100
  
  for ticker,minyear in tickers.items():
  #  print "TICKER %s" % ticker
    if minyear > 0 and minyear > year:
      continue
    
    r = get_ticker_data_from_web_stend(ticker + ".PA", start, end)    
    prices = r.close
    
    ratioInit = (prices[decisionTime]/prices[0]-1)*100;
    ratioFullYear = (prices[-1]/prices[0]-1)*100
  
    investYield = (prices[-1]/prices[decisionTime]-1)*100;
    
    results[ticker] = [ratioInit, ratioFullYear, investYield, prices[-1], prices[decisionTime], prices[0], prices]
                
  count = 0
  avgYield = 0
  index = 0
  stocksSorted = sorted(results.iteritems(), key=lambda (k,v): (v[0],k), reverse=pickBestStock)
  used = {}
  
  for key, value in stocksSorted:
      index += 1
  #    print "%s: %s" % (key, value)
      ratioInit       = value[0]
      ratioFullYear   = value[1]
      investYield     = value[2]
      stockYearValues = value[5]
      ticker = key
             
      if count < numStockInvested or (investInLastStock and index == len(stocksSorted)):
#        print "%3s : yield year=%7.2f y2invest=%7.2f, invest=%7.2f, %7.2f -- %7.2f -- %7.2f" % (ticker, ratioFullYear, ratioInit, 
#                                                                                       investYield, value[3], value[4], value[5])
        used[key] = 1
        avgYield += investYield
        count += 1
        
  # find worst drop after decision time
  usedStocks = []
  for t,v in results.iteritems():
    if used.has_key(t):
      decisionStockValue = v[6][decisionTime]
      tmp = [ e * 1000/decisionStockValue for e in v[6][decisionTime:] ]
      usedStocks.append(tmp)
#      print "%s %7.2f %7.2f %7.2f %i" % (t, tmp[-1], tmp[0], (tmp[-1]/tmp[0]-1)*100, len(tmp) )
      
  sumStocks = [sum(values) for values in zip(*usedStocks)]
  worstDrop = (min(sumStocks) / sumStocks[0] - 1) * 100    
  
#  print "-->> %7.2f / %7.2f" % (sumStocks[-1], sumStocks[0])          
  return  (year, avgYield/count, ratioCAC, ratioCACInit, worstDrop, ( sumStocks[-1] / sumStocks[0] - 1) * 100 )
  
investInLastStock = False
pickBestStock     = False

for  pickBestStock in [True, False]: 
  for decisionTime in range (0, 41, 40):
  
    for numStockInvested in range(20,41,20):
      gain = 1
    
      start = 2003
      end   = 2011
      
      for y in range(start, end):
        r = compute_performance(y)
        print "  %7i AVG YIELD = %.2f (cac40 = %.2f, with init %.2f), worst fall = %.2f, y=%.2f" % r
        
        g = -20.0 if r[1] < -20.0 else r[1]
        gain *= (1+g/100.0)
        
      print "==d=%i,#stock=%i,%s,best=%s== TOTAL gain = %.2f (ie %.2f per year)" % \
                    (decisionTime, numStockInvested, investInLastStock, pickBestStock,
                    (gain-1)*100, (math.pow(gain, 1.0/(end-start-1.0))-1)*100 if end-start-1.0 > 0 else gain)   
        
""" ---------------- MAIN PROGRAM -------------------- """          

