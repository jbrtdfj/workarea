'''
Created on 7 May 2016

@author: david
'''

import numpy as np

from talib import STOCH
from talib import SAR

class TickerIndicators():
  STO_LOW_K = "STO_LOW_K"
  STO_LOW_D = "STO_LOW_D"
  SARmCLOSE = "SARmCLOSE"
  SAR       = "SAR"

  def __init__(self, tickerData):
    self.data = tickerData

    self.stoch_slowk =  None
    self.stoch_slowd =  None
    self.sar         =  None

    self.usedIndicators = []
    self.curDateIndex   = None

  def activate(self, name):
    if name == TickerIndicators.STO_LOW_K:   val = self.get_stoch_slowk()
    elif name == TickerIndicators.STO_LOW_D: val = self.get_stoch_slowd()
    elif name == TickerIndicators.SARmCLOSE: val = self.get_sarmclose()
    elif name == TickerIndicators.SAR:       val = self.get_sar()
    
    else:
      print "ERROR indicator %s not defined"
      
    self.usedIndicators.append(val)
    
  '''--- INDICATORS ACCESS API ---------------------------------'''  

  def setCurDate(self, dateIndex):
    self.curDateIndex = dateIndex

  def value(self, indIndex, dateIndex=None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    return self.usedIndicators[indIndex][d]

  def greaterThan(self, indIndex, limit, dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    return self.usedIndicators[indIndex][d] > limit

  def lessThan(self, indIndex, limit, dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    return self.usedIndicators[indIndex][d] < limit

  def crossUp(self, indIndex, limit, dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    now = self.usedIndicators[indIndex][d]
    z1  = self.usedIndicators[indIndex][d-1]
    
    return (now > limit and z1 < limit)

  def crossDown(self, indIndex, limit, dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    now = self.usedIndicators[indIndex][d]
    z1  = self.usedIndicators[indIndex][d-1]
    
    return (now < limit and z1 > limit)

  def valueBetween(self, indIndex, minV, maxV, dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    now = self.usedIndicators[indIndex][d] 
    
    return (now < maxV and now > minV)

  def max(self, indIndex, limit=[1,1], dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    now = self.usedIndicators[indIndex][d]
    z1  = self.usedIndicators[indIndex][d-limit[1]]
    z2  = self.usedIndicators[indIndex][d-limit[0]-limit[1]]
    
    return (now < z1 and z1 > z2)

  def min(self, indIndex, limit=[1,1], dateIndex = None):
    d = self.curDateIndex if dateIndex is None else dateIndex
    now = self.usedIndicators[indIndex][d]
    z1  = self.usedIndicators[indIndex][d-limit[1]]
    z2  = self.usedIndicators[indIndex][d-limit[0]-limit[1]]
    
    return (now > z1 and z1 < z2)

  '''--- COMPUTE INDICATORS ---------------------------------'''  
  
  def computeSTOCH(self):
    ''' fill indicators array with its values '''

    self.stoch_slowk =  np.zeros(self.data.size(), dtype='f4')
    self.stoch_slowd =  np.zeros(self.data.size(), dtype='f4')
    
    d = self.data
    self.stoch_slowk, self.stoch_slowd = STOCH(d.high(), d.low(), d.close(), 
                                               fastk_period=14, 
                                               slowk_period=3, slowk_matype=0, slowd_period=4, slowd_matype=0)

  def get_stoch_slowd(self, i = None):
    if self.stoch_slowd is None: 
      self.computeSTOCH()

    return self.stoch_slowd if i is None else self.stoch_slowd[i]

  def get_stoch_slowk(self, i = None):
    if self.stoch_slowk is None: 
      self.computeSTOCH()

    return self.stoch_slowk if i is None else self.stoch_slowd[i]

  def computeSAR(self):
    ''' fill indicators array with its values '''

    self.sar  =  np.zeros(self.data.size(), dtype='f4')
    
    d = self.data
    self.sar = SAR(d.high(), d.low(), acceleration=0.02, maximum=0.2) 

  def get_sar(self, i = None):
    if self.sar is None: 
      self.computeSAR()

    return self.sar if i is None else self.sar[i]

  def get_sarmclose(self, i = None):
    if self.sar is None: 
      self.computeSAR()

    d = self.data
    v = self.sar - d.close()
    return v if i is None else v[i]
  