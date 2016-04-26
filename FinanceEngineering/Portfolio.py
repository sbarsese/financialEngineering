from numpy.random import normal
from math import exp
import matplotlib.pyplot as plt
class Portfolio(object):
    
    def __init__(self, mean, sigma, t = 1, startPrice = 1):
        self.mean = float(mean)
        self.sigma = float(sigma)
        self.value = float(startPrice)
        self.valueOverTime = [self.value]
        self.t = 1
        self.mu = mean+0.5*(self.sigma**2)
        
    def step (self,dt):
        #dz = normal(self.mean,self.std)
        #self.value = (1+self.mu*dt+self.sigma*dz*float(dt)**0.5)
        e = normal(self.mean,self.sigma)
        self.value = self.value*exp(self.mean*dt+self.sigma*e*(float(dt)**0.5))
        self.valueOverTime.append(self.value)
        return self.value
    def steps(self,dt,numOfSteps):
        es = normal(0,1,numOfSteps)
        for e in es:
            self.value = self.value*exp(self.mean*dt+self.sigma*e*(float(dt)**0.5))
            eee  =self.mean*dt+self.sigma*e*(float(dt)**0.5)
            self.valueOverTime.append(self.value)
        return self.value
    def getValuesOverTime(self):
        return self.valueOverTime
    
    def drawProfile(self,title=""):
        dates = [i for i in range(len(self.valueOverTime))]
        keywords = {"title":title}
        fig =plt.figure()
        ax1 = plt.subplot(1,1,1,**keywords)
        ax1.plot(dates,self.valueOverTime)
        return fig

    def addDrawToFig(self,fig):
        dates = [i for i in range(len(self.valueOverTime))]
        #ax1 = fig.add_subplot(1,1,1)
        ax1 = plt.subplot(1,1,1)
        ax1.plot(dates,self.valueOverTime)
        return fig
        
        