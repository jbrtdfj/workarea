'''
Created on Oct 24, 2010

@author: david
'''
class Broker:
  tradeCosts  = [ (0, 1100,  'fixed', 0.99), (1100, 1e9, 'percent', 0.09) ]
  setAlert      = 0
  executedAlert = 0.5
  
  def tradeCost(self, capital):
    for c in self.tradeCosts:
      min, max, type, rate = c
      if capital > min and capital < max:
        if (type == 'fixed'):
          return rate
        else:
          return capital * rate / 100
    print "ERROR in trade cost for capitalHistory = %f" % capital  
    return 100000 
