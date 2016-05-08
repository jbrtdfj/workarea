'''
Created on 7 May 2016

@author: david
'''

import numpy as np

from talib import STOCH

class TickerIndicators():

  def __init__(self, tickerData):
    self.data = tickerData

    self.stoch_slowk =  None
    self.stoch_slowd =  None

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
  