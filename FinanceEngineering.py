from FinanceEngineering.GetData import DataFetcher
import sys
import csv
import numpy
import matplotlib
import matplotlib.pyplot as plt
numpy.set_printoptions(linewidth=1000)
import Tkinter
import FileDialog
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
def printMatrix(symbols,matrix):
    matrix = matrix.getA()
    print "\t".join([" "] + symbols)
    for i in range(matrix.shape[0]):
        print symbols[i],"\t","\t".join([str(x) for x in list(matrix[i:i+1,][0])])
def generateOutput(sols,r_min,symbols,outputFile):
    sol = sols[r_min]
    if sol['status'] != 'optimal':
            print 'no solution found'
            return
    print "cov matrix:"
    print sol['sigma']
    #print type(numpy.array(sol['sigma']))
    #print numpy.array(sol['sigma'])
    
    printMatrix(symbols,numpy.matrix(sol['sigma']))
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
    
    plot_frontier(symbols,sols,r_min)
    plt.savefig("output.png")
    plt.show()
    '''means, stds = [],[]
    for i in range(len(symbols)):
        means.append(sol['returns'][i])
        stds.append(sol['sigma'][i,i]**0.5)

    fig = plt.figure()
    plt.plot(stds, means, 'o', markersize=5)
    
    #means.append(sol['return'])
    #stds.append(float(sol['var'])**0.5)
    #symbols.append("TOTAL")
    plt.plot(float(sol['var'])**0.5, sol['return'], 'y-o')
    ax = fig.add_subplot(111)
    for xy in zip(symbols,stds, means):
        ax.annotate('%s' % xy[0], xy=xy[1:], textcoords='data')
    ax.annotate('%s' % "TOTAL", xy=[float(sol['var'])**0.5, sol['return']], textcoords='data')
    plt.xlabel('std')
    plt.ylabel('mean')
    plt.title('Mean and standard deviation of returns of randomly generated portfolios')
    plt.show()'''
    
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
    args[0] = mv or dc or mvf
    args[1] = companies file (mv) or history data (mvf)
    args[2] = fromDate covariance DD-MM-YYYY E.g01-01-2015 (mv) or date idx of history (mvf)
    args[3] = toDate covariance DD-MM-YYYY E.g01-01-2015 (mv) or close price idx of history (mvf)
    args[4] = desired annual return
    args[5] = lambda . default 0
    args[6] = fromYear returns
    args[7] = outputfile'''
    print args
def main(args):
    
    if len(args) < 5 or (len(args) > 0 and (args[0] == 'help' or args[0] == 'h')):
        help(args)
        return
    method = 'dc' if args[0]=='dc' else 'mvf' if args[0]=='mvf' else 'mv'
    companiesFile = args[1]
    fromDate = args[2]
    toDate = args[3]
    #data,symbols = DataFetcher.GetCompaniesReturnsToDictYields(companiesFile, fromDate, toDate)
    data,symbols = DataFetcher.GetCompaniesFromHistFilesDirPath(companiesFile, int(fromDate),int(toDate)) if method == 'mvf' else DataFetcher.GetCompaniesReturnsToDictYields(companiesFile, fromDate, toDate)
    if method =='dc':
        lmbds =  DataFetcher.calculateBestLambdaForDynamicCov(data,symbols)
        for lmbda in sorted(lmbds.keys()):
            print lmbda,lmbds[lmbda]
    else:
        r_min = (1+float(args[4]))**(float(1)/251)-1
        lmbda = float(args[5]) if len(args) > 5 else 0
        fromYearReturns = int(args[6]) if len(args) > 6 else None
        outputFile = args[7] if len(args) > 7 else "output.csv"
        
        
        sols = {}
        try:
            #sol =  DataFetcher.meanVarianceOptimization(data,symbols,r_min,lmbda,fromYearReturns)
            sols[r_min] = DataFetcher.meanVarianceOptimization(data,symbols,r_min,lmbda,fromYearReturns)
            for r in [(1+r)**(float(1)/251)-1 for r in [0.015*x for x in range(1,100)]]:
                try:
                    
                    s = DataFetcher.meanVarianceOptimization(data,symbols,r,lmbda,fromYearReturns)
                    if s['status'] == 'optimal':
                        sols[r] = s
                    else:
                        returns = sorted(list(sols[r_min]['returns']),reverse= True)
                        r_max = sum(returns[:2] if len(returns) > 1 else returns[0])/(2 if len(returns) > 1 else 1)
                        s = DataFetcher.meanVarianceOptimization(data,symbols,r_max,lmbda,fromYearReturns)
                        sols[r_max] = s
                        break
                except Exception,e:
                    returns = sorted(list(sols[r_min]['returns']),reverse= True)
                    r_max = sum(returns[:2] if len(returns) > 1 else returns[0])/(2 if len(returns) > 1 else 1)
                    s = DataFetcher.meanVarianceOptimization(data,symbols,r_max,lmbda,fromYearReturns)
                    sols[r_max] = s
                    break
            generateOutput(sols,r_min,symbols,outputFile)
        except Exception,e:
            print e
if __name__ == '__main__':
    
    args = sys.argv[1:]
    main(args)
    
    
