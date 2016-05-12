'''
Created on 7 May 2016

@author: david
'''

class BackTester():
    '''
    classdocs
    '''
  
    def __init__(self, tickerData, strategy):
      self.ticker   = tickerData
      self.strategy = strategy

    def run(self):
      self.strategy.prepare();
      
      for time in range(1,self.ticker.size()):
        self.strategy.runTime(time)
        
      print "%-30s Total Gain : %.0f (%2.1f%s)" % (self.strategy.name, self.strategy.totalGain(), self.strategy.totalGain(1), "%")
        
