import csv
import sys
import matplotlib.pyplot as plt
import numpy

stockFile = sys.path[0] + "/../data/cac40_data.csv"

f      = open(stockFile, 'r')
reader = csv.DictReader(f, delimiter=',')

init = 1
stockValuesShifted = []

print "# read data"
#--- load stock value 
stockValues = [float(line['Open']) for line in reader]

initStock = stockValues[len(stockValues)-1]

stockValues.reverse()
stockValues = stockValues[4800:]     # low: 3300 peak:2500

stockValuesShifted = [x-initStock for x in stockValues]

numDataPoints = len(stockValuesShifted)
numDataRange = range(numDataPoints)

print "average stock " + str(numpy.mean(stockValuesShifted))

print "# end read data"

 
print "# simulate average investement"
resultAvgInvestmentGain   = []

timeOfCapital = 0
resultCapitalOverTime   = []
resultCapitalGainOverTime = []
resultInvestOverTime      = []
resultAvgPerfOverTime     = []

daysBetweenInvestment = 30   # day
investment            = 1.0 * daysBetweenInvestment;

startStockValue = stockValues[0]

for startInvestTime in range(numDataPoints): 
  investmentTotal       = 1.0
  capital               = 1.0
  previousValue         = stockValues[startInvestTime]
   
  if (startInvestTime < timeOfCapital):
    resultCapitalOverTime.append += [0.0] * daysBetweenInvestment
    resultCapitalGainOverTime    += [0.0] * daysBetweenInvestment
    resultInvestOverTime         += [0.0] * daysBetweenInvestment
    resultAvgPerfOverTime        += [0.0] * daysBetweenInvestment
     
  for time in range(startInvestTime+1, numDataPoints, daysBetweenInvestment):
    capital         *= ( 1 + ((stockValues[time] - previousValue) / previousValue) )
    previousValue    = stockValues[time]

    if (startInvestTime == timeOfCapital):
      resultCapitalOverTime += [capital] * daysBetweenInvestment
      resultInvestOverTime += [investmentTotal] * daysBetweenInvestment
      
      avgGain = (capital / investmentTotal - 1) * 100.0
      resultCapitalGainOverTime += [avgGain] * daysBetweenInvestment
      
      absGain = (stockValues[time]-startStockValue) / startStockValue * 100
      resultAvgPerfOverTime        += [absGain] * daysBetweenInvestment

    investmentTotal += investment
    capital         += investment
    
  if (investmentTotal != 0):
    resultAvgInvestmentGain.append( (capital / investmentTotal - 1) * 100.0)

    
plt.plot(
         numDataRange, [x/100 for x in stockValues], 
#         range(len(resultAvgInvestmentGain)), resultAvgInvestmentGain,
#         range(len(resultCapitalOverTime)), [x/100.0 for x in resultCapitalOverTime],
#         range(len(resultCapitalGainOverTime)), resultCapitalGainOverTime,
#         range(len(resultInvestOverTime)), [x/100.0 for x in resultInvestOverTime],
#         range(len(resultAvgPerfOverTime)), resultAvgPerfOverTime,
#         range(len(resultAvgPerfOverTime)), [0] * len(resultAvgPerfOverTime)
         )
  
plt.show()
