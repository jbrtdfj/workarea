'''
Created on Oct 24, 2010

@author: david
'''

import numpy as np
import datetime
import matplotlib.finance as finance
import matplotlib.mlab    as mlab


def get_ticker_data_from_web(ticker):
  """  return a numpy record array with fields: date, open, high, low, close, volume, adj_close) """
  startdate = datetime.date(1990,1,1)
  enddate   = datetime.date.today()
  
  fh = finance.fetch_historical_yahoo(ticker, startdate, enddate)
  
  r = mlab.csv2rec(fh); fh.close()
  r.sort()

  return r

def get_ticker_data_from_web_stend(ticker, startdate, enddate):
  """  return a numpy record array with fields: date, open, high, low, close, volume, adj_close) """
  
  fh = finance.fetch_historical_yahoo(ticker, startdate, enddate)
  
  r = mlab.csv2rec(fh); fh.close()
  r.sort()

  return r

def get_ticker_data_from_file(ticker):
  import sys
  
  stockFile = sys.path[0] + "/../data/%s_data.csv" % (ticker) 
  
  f      = open(stockFile, 'r')
  
  r = mlab.csv2rec(f); f.close()
  r.sort()

  return r

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    if (len(a) >= n):
      a[:n] = a[n]
    else:
      a[:len(a)-1] = a[len(a)-1]
    return a
