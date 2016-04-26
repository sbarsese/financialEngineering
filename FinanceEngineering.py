from FinanceEngineering.GetData import DataFetcher
from FinanceEngineering.PorfolioOptimization import PortfolioOptimization
from FinanceEngineering.StockAnalysis import StockAnalysis
import sys
import csv
import numpy
import matplotlib
import matplotlib.pyplot as plt
import Tkinter
import FileDialog
from FinanceEngineering.Portfolio import Portfolio
from FinanceEngineering.PlotsGenerator import PlotsGenerator
numpy.set_printoptions(linewidth=1000)
'''def plot_frontier(symbols,sols,r_min):
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
    for solR in sols:
        sol1= sols[solR]
        xyPoint = [float(sol1['var'])**0.5, sol1['return']]
        plt.plot(xyPoint[0],xyPoint[1], 'ro' if solR == r_min else 'y-o' )
        ax.annotate('%s_%f' % ("T",(1+solR)**251), xy=xyPoint, textcoords='data')
    plt.xlabel('std')
    plt.ylabel('mean')
    plt.title('daily return (Mean) and standard deviation of returns')
    #plt.show()
def printMatrix(symbols,matrix):
    matrix = matrix.getA()
    print "\t".join([" "] + symbols)
    for i in range(matrix.shape[0]):
        print symbols[i],"\t","\t".join([str(x) for x in list(matrix[i:i+1,][0])])'''
def generateOutput(sols,r_min,symbols,outputFile):
    sol = sols[r_min]
    if sol['status'] != 'optimal':
            print 'no solution found'
            return
    print "cov matrix:"
    print sol['sigma']
    #print type(numpy.array(sol['sigma']))
    #print numpy.array(sol['sigma'])
    
    PlotsGenerator.printMatrix(symbols,numpy.matrix(sol['sigma']))
    print "returns:\r\n"
    for ret in  zip(symbols,sol['returns']):
        print ret[0],"\t",ret[1]
    
    print "total daily return:"
    print sol['return']

    print "total ANNUAL return:"
    print (1+sol['return'])**251
    
    print "weights:"
    weights = {symbol[0]:symbol[1] for symbol in zip(symbols,[float(x) for x in sol['x']])}
    for symbol in weights:
        print symbol,"\t",weights[symbol],"\t",weights[symbol]*100
    print'var:'
    print sol['var']
    
    PlotsGenerator.plot_frontier(symbols,sols,r_min)
    plt.savefig("frontier.png")
    plt.show()
    
    '''idxOfSp = 0
    for i in range(len(symbols)):
        if "sp500" in symbols[i]:
            idxOfSp = i
            break
    portfolio = Portfolio(float(sol['returns'][idxOfSp]),float(sol['sigma'][idxOfSp,idxOfSp])**0.5)
    portfolio.steps(1, 365)
    figg1 = portfolio.drawProfile()
    plt.show() '''
    
    portfolio = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    portfolio.steps(1, 365)
    p1 = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    p1.steps(1, 365)
    p2 = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    p2.steps(1, 365)
    figg = portfolio.drawProfile("3 realizations - 8 years")
    p1.addDrawToFig(figg)
    p2.addDrawToFig(figg)
    #figg.
    plt.savefig("3Realizations.png")
    plt.show()  
    figg = portfolio.drawProfile("some realizations - 8 years")
    pors = [Portfolio(float(sol['return']),float(sol['var'])**0.5) for i in range(500)]
    i=0
    for por in pors:
        i+=1
        por.steps(1, 365)
        if i< 15:
            por.addDrawToFig(figg)
    print "realizations: ",[por.value for por in pors]
    plt.savefig("SomeRealizations.png")
    plt.show()  
    avgDailyReturn = sum((por.value-1)/len(por.valueOverTime) for por in pors)/len(pors)
    print "avg return: ",avgDailyReturn,(1+avgDailyReturn)**251
    
    
    
    pDaily = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    pDaily.steps(float(1)/float(24), 24)
    figg = portfolio.drawProfile("daily change")
    pDaily1 = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    pDaily1.steps(float(1)/float(24), 24)
    pDaily2 = Portfolio(float(sol['return']),float(sol['var'])**0.5)
    pDaily2.steps(float(1)/float(24), 24)
    pDaily1.addDrawToFig(figg)
    pDaily2.addDrawToFig(figg)
    plt.savefig("DailyRealizations.png")
    plt.show()
    
    with open (outputFile,"wb") as file:
        writer = csv.writer(file)
        writer.writerow(["returns"])
        for ret in zip(symbols,sol['returns']):
            writer.writerow(list(ret))
        writer.writerow(["weights"])
        for symbol in weights:
            writer.writerow([symbol,weights[symbol]])
        writer.writerow(["total daily return",sol['return']])
        writer.writerow(["total annual return",(1+sol['return'])**251])
        writer.writerow(["total var",sol['var']])
def help(args):
    print ''''error:
    args[0] = mv (mean variance optimization) or dc (dynamic covariance factor) or mvf (mean variance optimization files) or sp (simlate portfolio)
    args[1] = companies file (mv) or history data (mvf) or mean(sp)
    args[2] = fromDate covariance DD-MM-YYYY E.g01-01-2015 (mv) or date idx of history (mvf) or std(sp)
    args[3] = toDate covariance DD-MM-YYYY E.g01-01-2015 (mv) or close price idx of history (mvf) or dt(sp)
    args[4] = desired annual return or periods(sp)
    args[5] = lambda . default 0 or numOfTrails(Sp)
    args[6] = fromYear returns
    args[7] = outputfile'''
    print args
def main(args):
    if len(args) < 5 or (len(args) > 0 and (args[0] == 'help' or args[0] == 'h')):
        help(args)
        return
    method = 'dc' if args[0]=='dc' else 'mvf' if args[0]=='mvf' else 'sp' if args[0]=='sp' else 'mv'
    if method =='sp':
        mean = float(args[1])
        std = float(args[2])
        dt = float(args[3])
        periods = int(args[4])
        trails = int(args[5]) if len(args) > 0 else 1
        if trails == 1:
            portfolio = Portfolio(mean,std)
            portfolio.steps(1, 365)
            figg = portfolio.drawProfile()
            plt.show()
        else:
            results = []
            mainPortfolio = Portfolio(mean,std)
            figg = mainPortfolio.drawProfile()
            i = 0
            for trail in range(trails):
                i+=1
                portfolio = Portfolio(mean,std)
                portfolio.steps(1, 365)
                if i < 10:
                    portfolio.addDrawToFig(figg)
                results.append(portfolio.value)
            print "realizations:",results
            print "Avg:",sum(results)/len(results)
            plt.show()
        return
    companiesFile = args[1]
    fromDate = args[2]
    toDate = args[3]
    #data,symbols = DataFetcher.GetCompaniesReturnsToDictYields(companiesFile, fromDate, toDate)
    data,symbols = DataFetcher.GetCompaniesReturnsFromHistFilesDirPath(companiesFile, int(fromDate),int(toDate)) if method == 'mvf' else DataFetcher.GetCompaniesReturnsToDict(companiesFile, fromDate, toDate,"outputReturns.csv")
    
    
    
    if method =='dc':
        lmbds =  StockAnalysis.calculateBestLambdaForDynamicCov(data,symbols)
        for lmbda in sorted(lmbds.keys()):
            print lmbda,lmbds[lmbda]
            
    else: # mv || mvf
        r_min = (1+float(args[4]))**(float(1)/251)-1
        lmbda = float(args[5]) if len(args) > 5 else 0
        fromYearReturns = int(args[6]) if len(args) > 6 else None
        outputFile = args[7] if len(args) > 7 else "output.csv"
        sols = {}
        try:
            #sol =  DataFetcher.meanVarianceOptimization(data,symbols,r_min,lmbda,fromYearReturns)
            sols[r_min] = PortfolioOptimization.meanVarianceOptimization(data,symbols,r_min,lmbda,fromYearReturns)
            for r in [(1+r)**(float(1)/251)-1 for r in [0.015*x for x in range(1,100)]]:
                try:
                    
                    s = PortfolioOptimization.meanVarianceOptimization(data,symbols,r,lmbda,fromYearReturns)
                    if s['status'] == 'optimal':
                        sols[r] = s
                    else:
                        returns = sorted(list(sols[r_min]['returns']),reverse= True)
                        r_max = sum(returns[:2] if len(returns) > 1 else returns[0])/(2 if len(returns) > 1 else 1)
                        s = PortfolioOptimization.meanVarianceOptimization(data,symbols,r_max,lmbda,fromYearReturns)
                        sols[r_max] = s
                        break
                except Exception,e:
                    returns = sorted(list(sols[r_min]['returns']),reverse= True)
                    r_max = sum(returns[:2] if len(returns) > 1 else returns[0])/(2 if len(returns) > 1 else 1)
                    s = PortfolioOptimization.meanVarianceOptimization(data,symbols,r_max,lmbda,fromYearReturns)
                    sols[r_max] = s
                    break
            generateOutput(sols,r_min,symbols,outputFile)
        except Exception,e:
            print e
if __name__ == '__main__':
    
    args = sys.argv[1:]
    main(args)
    
    
