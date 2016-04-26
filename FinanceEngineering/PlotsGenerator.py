import matplotlib
import matplotlib.pyplot as plt

import Tkinter
import FileDialog

class PlotsGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def plot_frontier(symbols,sols,r_min):
        sol = sols[r_min]
        means, stds = [],[]
        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(111)
        for i in range(len(symbols)):
            #means.append(sol['returns'][i])
            means.append(sol['returns'][i])
            stds.append(sol['sigma'][i,i]**0.5)
    
    
        plt.plot(stds, means, 'o', markersize=5)
        #plt.plot(float(sol['var'])**0.5, sol['return'], 'y-o')
        
        for xy in zip(symbols,stds, means):
            ax.annotate('%s' % xy[0], xy=xy[1:], textcoords='data')
        #ax.annotate('%s' % "TOTAL", xy=[float(sol['var'])**0.5, sol['return']], textcoords='data')
        
        '''ret = [float(sols[solR]['return']) for solR in sols]
        risk = [float(sols[solR]['var'])**0.5 for solR in sols]
        fit = numpy.polyfit(ret, [r**2 for r in risk], 2)
        fit_fn = numpy.poly1d(fit) 
    
        plt.plot(risk,ret, 'yo', risk, fit_fn(risk), '--k')'''
        for solR in sols:
            sol1= sols[solR]
            xyPoint = [float(sol1['var'])**0.5, sol1['return']]
            plt.plot(xyPoint[0],xyPoint[1], 'ro' if solR == r_min else 'y-o' )
            ax.annotate('%s_%f' % ("T",(1+solR)**251), xy=xyPoint, textcoords='data')
        plt.xlabel('std')
        plt.ylabel('mean')
        plt.title('daily return (Mean) and standard deviation of returns')
        #plt.show()
    @staticmethod
    def printMatrix(symbols,matrix):
        matrix = matrix.getA()
        print "\t".join([" "] + symbols)
        for i in range(matrix.shape[0]):
            print symbols[i],"\t","\t".join([str(x) for x in list(matrix[i:i+1,][0])])
        