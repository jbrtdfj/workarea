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
      for time in range(20,self.ticker.size()):
        self.strategy.runTime(time)
        
