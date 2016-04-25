import urllib2
import json
import time
import csv
import urllib
import urllib2
import os
import pickle
import glob
import codecs
import sys
import csv
import math
import numpy as np
import numpy
from cvxopt import matrix
from cvxopt.solvers import qp, options
import sys
from os import listdir
from os.path import isfile, join
options['show_progress'] = False
sys.path.append("C:\Python27\lib\site-packages\cvxopt")
class DataFetcher(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def GetCompaniesToFile(companiesFile, startDate, endDate, outputFolder):
        symbols = []
        startDate = startDate.split("-")
        endDate = endDate.split("-")
        # csvaddressTemplate="http://ichart.yahoo.com/table.csv?s={0}&a=11&b=31&c=2012&d=11&e=31&f=2013&g=d&ignore=.csv"
        csvaddressTemplate = "http://ichart.yahoo.com/table.csv?s={0}" + "&a={0}&b={1}&c={2}&d={3}&e={4}&f={5}&g=d&ignore=.csv".format(str(int(startDate[1]) - 1), startDate[0], startDate[2], str(int(endDate[1]) - 1), endDate[0], endDate[2])
        templateOutput = "{0}/{1}_{2}_{3}.csv"
        with open(companiesFile, 'rb') as file:
            reader = csv.reader(file)
            symbols = [line[0] for line in reader]
            print symbols
        for symbol in symbols:

            request = csvaddressTemplate.format(symbol)
            # print csvaddress1
            urllib.urlretrieve (request, templateOutput.format(outputFolder, symbol, "".join(startDate), "".join(endDate)))
            file = urllib.urlopen(request)
            print file.readlines()
            
            print request
            
    @staticmethod
    def GetCompaniesToDict(companiesFile, startDate, endDate):
        retDict = {}
        symbols = []
        startDate = startDate.split("-")
        endDate = endDate.split("-")
        # csvaddressTemplate="http://ichart.yahoo.com/table.csv?s={0}&a=11&b=31&c=2012&d=11&e=31&f=2013&g=d&ignore=.csv"
        csvaddressTemplate = "http://ichart.yahoo.com/table.csv?s={0}" + "&a={0}&b={1}&c={2}&d={3}&e={4}&f={5}&g=d&ignore=.csv".format(str(int(startDate[1]) - 1), startDate[0], startDate[2], str(int(endDate[1]) - 1), endDate[0], endDate[2])
        with open(companiesFile, 'rb') as file:
            reader = csv.reader(file)
            symbols = [line[0] for line in reader]
            print symbols
        for symbol in symbols:

            request = csvaddressTemplate.format(symbol)
            # print csvaddress1
            # urllib.urlretrieve (request, templateOutput.format(outputFolder,symbol,"".join(startDate),"".join(endDate)))
            response = urllib.urlopen(request)
            data = [line.rstrip().split(',') for line in response.readlines()]
            retDict[symbol] = data
        return retDict, symbols
    
    
    @staticmethod
    def GetCompaniesFromHistFilesDirPath(histFilesDirPath,dateIdx=0,closePriceIdx=1):
        histFilesDirPath = histFilesDirPath.replace(r'\\',os.sep)
        retDict = {}
        symbols = []
        files = [f for f in listdir(histFilesDirPath) if isfile(join(histFilesDirPath, f))]
        for fileName in sorted(files):
            symbol = fileName.replace(".csv","")
            symbols.append(symbol)
            filePath = join(histFilesDirPath, fileName)
            with open(filePath, 'rb') as file:
                reader = csv.reader(file)
                data = [[line[dateIdx],line[closePriceIdx]] for line in reader][1:]
                for i in range(len(data) - 1):
                    date = data[i][0]
                    dateParts = date.split("/") if "/" in date else date.split("-")
                    dateParts = reversed(dateParts) if len(dateParts[-1]) == 4 else dateParts
                    date = "-".join(dateParts)
                    ret = math.log(float(data[i][1]) / float(data[i + 1][1]))
                    if date not in retDict:
                        retDict[date] = {}
                    retDict[date][symbol] = ret
        return retDict,symbols
                
                    
    @staticmethod
    def GetCompaniesToDictYields(companiesFile, startDate, endDate, outputFile):
        retDict = {}
        symbols = []
        startDate = startDate.split("-")
        endDate = endDate.split("-")
        # csvaddressTemplate="http://ichart.yahoo.com/table.csv?s={0}&a=11&b=31&c=2012&d=11&e=31&f=2013&g=d&ignore=.csv"
        csvaddressTemplate = "http://ichart.yahoo.com/table.csv?s={0}" + "&a={0}&b={1}&c={2}&d={3}&e={4}&f={5}&g=d&ignore=.csv".format(str(int(startDate[1]) - 1), startDate[0], startDate[2], str(int(endDate[1]) - 1), endDate[0], endDate[2])
        with open(companiesFile, 'rb') as file:
            reader = csv.reader(file)
            symbols = [line[0] for line in reader]
            print symbols
        for symbol in symbols:
            request = csvaddressTemplate.format(symbol)
            # print csvaddress1
            # urllib.urlretrieve (request, templateOutput.format(outputFolder,symbol,"".join(startDate),"".join(endDate)))
            response = urllib.urlopen(request)
            data = [line.rstrip().split(',') for line in response.readlines()][1:]
            for i in range(len(data) - 1):
                date = data[i][0]
                ret = math.log(float(data[i][4]) / float(data[i + 1][4]))
                if date not in retDict:
                    retDict[date] = {}
                retDict[date][symbol] = ret
        symbolIdx = zip(symbols, [idx for idx in range(len(symbols))])
        print symbolIdx
        with open (outputFile, "wb") as file:
            writer = csv.writer(file)
            writer.writerow(["date"] + [symbolIdx[i][0] for i in range(len(symbolIdx))])
            for date in sorted(retDict.keys(), key=lambda d: map(int, d.split('-'))):
                writer.writerow([date] + [retDict[date][symbolIdx[i][0]] if symbolIdx[i][0] in retDict[date] else "" for i in range(len(symbolIdx))])    
        return retDict
    
    @staticmethod
    def GetCompaniesReturnsToDictYields(companiesFile, startDate, endDate):
        retDict = {}
        symbols = []
        startDate = startDate.split("-")
        endDate = endDate.split("-")
        # csvaddressTemplate="http://ichart.yahoo.com/table.csv?s={0}&a=11&b=31&c=2012&d=11&e=31&f=2013&g=d&ignore=.csv"
        csvaddressTemplate = "http://ichart.yahoo.com/table.csv?s={0}" + "&a={0}&b={1}&c={2}&d={3}&e={4}&f={5}&g=d&ignore=.csv".format(str(int(startDate[1]) - 1), startDate[0], startDate[2], str(int(endDate[1]) - 1), endDate[0], endDate[2])
        with open(companiesFile, 'rb') as file:
            reader = csv.reader(file)
            symbols = [line[0] for line in reader]
            print symbols
        for symbol in symbols:
            request = csvaddressTemplate.format(symbol)
            # print csvaddress1
            # urllib.urlretrieve (request, templateOutput.format(outputFolder,symbol,"".join(startDate),"".join(endDate)))
            response = urllib.urlopen(request)
            data = [line.rstrip().split(',') for line in response.readlines()][1:]
            for i in range(len(data) - 1):
                date = data[i][0]
                ret = math.log(float(data[i][4]) / float(data[i + 1][4]))
                if date not in retDict:
                    retDict[date] = {}
                retDict[date][symbol] = ret
        symbolIdx = zip(symbols, [idx for idx in range(len(symbols))])
        print symbolIdx
        return retDict, symbols
    @staticmethod
    def getCovarianceMatrix(vector1, vector2):
        return np.cov(np.vstack(vector1, vector2))
    @staticmethod
    def getCovarianceMatrixByNames(data, symbol1, symbol2):
        # print data
        lists = [(data[date][symbol1], data[date][symbol2]) for date in data if symbol1 in data[date] and symbol2 in data[date]]
        # print lists
        return np.cov(np.vstack(([x[0] for x in lists], [x[1] for x in lists]))) if len(lists) >0 else [[0,0],[0,0]]
    @staticmethod
    def f(dateDict, symbols):
        for symbol in symbols:
            if symbol not in dateDict:
                return False
        return True
    
    @staticmethod
    def getCovarianceMatrixBySymbolsList(data, symbols):
        # print data
        
        covMatrx = [[0 for i in range(len(symbols))] for i in range(len(symbols))]
        #print covMatrx
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                S1S2covMatrix = DataFetcher.getCovarianceMatrixByNames(data, symbols[i], symbols[j])
                if i == j:
                    covMatrx[i][i] = S1S2covMatrix[0][0]
                covMatrx[i][j] = S1S2covMatrix[0][1]
                covMatrx[j][i] = S1S2covMatrix[1][0]
        covMatrx = np.matrix(covMatrx)
        # print covMatrx
        return covMatrx
        '''sharedReturns = {symbol:[] for symbol in symbols}
        
        data = { date: data[date] for date in data if DataFetcher.f(data[date],symbols)}
        print len(data)
        for date in data:
            for symbol in symbols:
                sharedReturns[symbol].append(data[date][symbol])
        #lists = [[data1[date][symbol] for symbol in symbols] for date in data1]
        #print lists
        print [symbol for symbol in symbols]
        lists1 = (sharedReturns[symbol] for symbol in symbols)
        return np.cov(np.vstack(lists1))'''
   
   
    @staticmethod
    def getDynamicCovarianceMatrixBySymbolsListasList(data, symbols,lmbda = 0.03):
        print 'dynamic'
        covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
        dataPerMonth = {}
        symbolsPerMonth = {}
        months = {}
        for date in data.keys():
            dateKey = int("".join(date.split("-")[:2]))
            if dateKey not in dataPerMonth:
                dataPerMonth[dateKey] = {}
                symbolsPerMonth[dateKey] = set()
            dataPerMonth[dateKey][date] = data[date]
            for symbol in  dataPerMonth[dateKey][date]:
                symbolsPerMonth[dateKey].add(symbol)
        datesSorted = sorted(dataPerMonth.keys())
        monthsToInclude = 0
        for i in range(len(datesSorted)):
            dateKey = datesSorted[i]
            if len(symbolsPerMonth[dateKey]) == len(symbols):
                minDateKeyIdx = i+1
                print dateKey
                break
            
        '''for t in datesSorted[:-1]:
            covMatrx = lmbda*np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataPerMonth[t],symbols)) + (1-lmbda)*covMatrx
        covMatrixT = np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataPerMonth[datesSorted[-1]],symbols))
        
        
        dataAllT_1 = {}
        for t in datesSorted[:-1]:
            dataAllT_1.update(dataPerMonth[t])
        covMatrx = np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataAllT_1,symbols))
        x = sum(sum(abs(covMatrx.item((i,j))-covMatrixT.item((i,j))) for j in range(len(symbols))) for i in range(len(symbols)))
        print x'''
        #covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
        
        for t in datesSorted[minDateKeyIdx:]:
            #print t
            covMatrx = lmbda*np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataPerMonth[t],symbols)) + (1-lmbda)*covMatrx
        return covMatrx
    
    @staticmethod
    def calculateBestLambdaForDynamicCov(data, symbols,maxLambda = 0.1,dLmbda = 0.01):
        res = {}
        covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
        dataPerMonth = {}
        months = {}
        for date in data.keys():
            dateKey = int("".join(date.split("-")[:2]))
            if dateKey not in dataPerMonth:
                dataPerMonth[dateKey] = {}
            dataPerMonth[dateKey][date] = data[date]
        datesSorted = sorted(dataPerMonth.keys())
        lmbda = 0.01
        [0.01+i*dLmbda for i in range(15)]
        for lmbda in [i*dLmbda for i in range(11)]:
            #print lmbda
            covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
            for t in datesSorted[:-1]:
                covMatrx = lmbda*np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataPerMonth[t],symbols)) + (1-lmbda)*covMatrx
            covMatrixT = np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataPerMonth[datesSorted[-1]],symbols))
            res[lmbda] = sum(sum(abs(covMatrx.item((i,j))-covMatrixT.item((i,j))) for j in range(len(symbols))) for i in range(len(symbols)))
        dataAllT_1 = {}
        for t in datesSorted[:-1]:
            dataAllT_1.update(dataPerMonth[t])
        covMatrx = np.matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(dataAllT_1,symbols))
        res[0] = sum(sum(abs(covMatrx.item((i,j))-covMatrixT.item((i,j))) for j in range(len(symbols))) for i in range(len(symbols)))
        
        return res
    @staticmethod
    def getCovarianceMatrixBySymbolsListasList(data, symbols):
        # print data
        
        covMatrx = [[0 for i in range(len(symbols))] for i in range(len(symbols))]
        #print covMatrx
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                S1S2covMatrix = DataFetcher.getCovarianceMatrixByNames(data, symbols[i], symbols[j])
                if i == j:
                    covMatrx[i][i] = S1S2covMatrix[0][0]
                covMatrx[i][j] = S1S2covMatrix[0][1]
                covMatrx[j][i] = S1S2covMatrix[1][0]
        return covMatrx
        # print covMatrx
       
    @staticmethod
    def getReturnsSymbolsList(data, symbols, returnsFromYear=None):
        # print data
        returns = [0 for i in range(len(symbols))]
        for i in range(len(symbols)):
            symbol = symbols[i]
            dataSymbol = [data[date][symbol] for date in data if symbol in data[date] and (not returnsFromYear or int(date.split('-')[0]) >= returnsFromYear)]
            returns[i] = sum(dataSymbol) / len(dataSymbol) if len(dataSymbol) > 0 else 1
        return returns
    @staticmethod
    def meanVarianceOptimization(data, symbols, r_min,lmbda = 0, returnsFromYear=None):
        n = len(symbols)
        returns = DataFetcher.getReturnsSymbolsList(data, symbols, returnsFromYear)
        P = matrix(DataFetcher.getCovarianceMatrixBySymbolsListasList(data, symbols)) if lmbda <=0 else matrix(DataFetcher.getDynamicCovarianceMatrixBySymbolsListasList(data, symbols,lmbda))
        q = matrix(np.zeros((n, 1)))
        G = matrix(numpy.concatenate((
             np.array([[-x for x in returns]]),
             - numpy.identity(n))))
        minX = numpy.zeros((n, 1))
        minX[i,0] = 0.6
        h = matrix(numpy.concatenate((
             -numpy.ones((1, 1)) * r_min,
              numpy.zeros((n, 1))), 0))
        r_avg = np.identity(n)
        for i in range(len(returns)):
            r_avg[i][i] = returns[i]
        
        # equality constraint Ax = b; captures the constraint sum(x) == 1
        A = matrix(1.0, (1, n))
        b = matrix(1.0)
        '''print "P",P
        print "q",q
        print "G",G
        print "h",h
        print "A",A
        print "b",b'''
        x = np.array([-x for x in returns])
        sol = qp(P, q, G, h, A, b)
        x = np.matrix(sol['x'])
        sol['var'] = x.T * np.matrix(P) * x  
        sol['sigma'] = P 
        sol['returns'] = returns
        sol['return'] = returns * x
        return sol
