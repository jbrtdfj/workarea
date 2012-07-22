import csv
import sys
import matplotlib.pyplot as plt
import numpy

stockFile = sys.path[0] + "/../data/cac40_data.csv"

f      = open(stockFile, 'r')
reader = csv.DictReader(f, delimiter=',')

init = 1

print "# read data"
#--- load stock value 
stockValues = [[float(line['Open']), float(line['Close']), float(line['Low']) ] for line in reader]

stockValues = stockValues[:]

gain = []
loss = []

for data in stockValues:
  close = data[1]
  open  = data[0]
  
  if (close > open):
    gain.append((close - open)/open*100)
  else:
    loss.append((open - close)/open*100)
     
print "gain " + str(numpy.mean(gain))    
print "loss " + str(numpy.mean(loss))    
    

plt.hist(gain, 50, normed=1, facecolor='green', alpha=0.55)    
plt.hist(loss, 50, normed=1, facecolor='red', alpha=0.55)    
#plt.hist(gain, 50, normed=1, facecolor='red', alpha=0.75, cumulative = 'true')    
#    
plt.show()
