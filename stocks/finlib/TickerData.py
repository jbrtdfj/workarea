'''
Created on 2 May 2016

@author: david
'''
import matplotlib.finance as finance
import matplotlib.mlab    as mlab

import datetime

class TickerData:
    '''
    name
    share
    data
    '''
    
    def __init__(self, name, year, priceRatio=1):
      self.name       = name
      self.year       = year
      self.dataLoaded = 0
      self.data       = None
      self.priceRatio = priceRatio
        
    def getData(self):
      self.dataLoaded = 1

      startdate = datetime.date(self.year, 1, 1)
      enddate   = datetime.date(self.year, 12, 31)

      fh = finance.fetch_historical_yahoo(self.name, startdate, enddate)
  
      self.data = mlab.csv2rec(fh); fh.close()
      self.data.sort()

    def close(self, time=None):
      return self.data.close

    def closePrice(self, dateIndex):
      return self.data.close[dateIndex]/self.priceRatio
    
    def open(self):
      return self.data.open

    def openPrice(self, dateIndex):
      return self.data.open[dateIndex]/self.priceRatio

    def low(self):
      return self.data.low

    def lowPrice(self, dateIndex):
      return self.data.low[dateIndex]/self.priceRatio

    def high(self):
      return self.data.high

    def highPrice(self, dateIndex):
      return self.data.high[dateIndex]/self.priceRatio
      
    def gain(self):
      if self.dataLoaded == 0: self.getData()
      
      d = self.data.close
      res = [float(d[0]), float(d[-1]), 0]
      res[2] = (res[1]/res[0]-1)*100
      return res
    
    def size(self):
      return self.data.size
