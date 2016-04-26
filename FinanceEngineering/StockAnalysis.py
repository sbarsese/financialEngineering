import numpy as np
from GetData import DataFetcher
class StockAnalysis(object):


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def getCovarianceMatrix(vector1, vector2):
        return np.cov(np.vstack(vector1, vector2))
    @staticmethod
    def getCovarianceMatrixByNames(data, symbol1, symbol2):
        # print data
        lists = [(data[date][symbol1], data[date][symbol2]) for date in data if symbol1 in data[date] and symbol2 in data[date]]
        # print lists
        return np.cov(np.vstack(([x[0] for x in lists], [x[1] for x in lists]))) if len(lists) > 0 else [[0, 0], [0, 0]]
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
        # print covMatrx
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                S1S2covMatrix = StockAnalysis.getCovarianceMatrixByNames(data, symbols[i], symbols[j])
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
    def getDynamicCovarianceMatrixBySymbolsListasList(data, symbols, lmbda=0.03):
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
                minDateKeyIdx = i + 1
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
        # covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
        
        for t in datesSorted[minDateKeyIdx:]:
            # print t
            covMatrx = lmbda * np.matrix(StockAnalysis.getCovarianceMatrixBySymbolsListasList(dataPerMonth[t], symbols)) + (1 - lmbda) * covMatrx
        return covMatrx
    
    @staticmethod
    def calculateBestLambdaForDynamicCov(data, symbols, maxLambda=0.1, dLmbda=0.01):
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
        [0.01 + i * dLmbda for i in range(15)]
        for lmbda in [i * dLmbda for i in range(11)]:
            # print lmbda
            covMatrx = np.matrix([[0 for i in range(len(symbols))] for i in range(len(symbols))])
            for t in datesSorted[:-1]:
                covMatrx = lmbda * np.matrix(StockAnalysis.getCovarianceMatrixBySymbolsListasList(dataPerMonth[t], symbols)) + (1 - lmbda) * covMatrx
            covMatrixT = np.matrix(StockAnalysis.getCovarianceMatrixBySymbolsListasList(dataPerMonth[datesSorted[-1]], symbols))
            res[lmbda] = sum(sum(abs(covMatrx.item((i, j)) - covMatrixT.item((i, j))) for j in range(len(symbols))) for i in range(len(symbols)))
        dataAllT_1 = {}
        for t in datesSorted[:-1]:
            dataAllT_1.update(dataPerMonth[t])
        covMatrx = np.matrix(StockAnalysis.getCovarianceMatrixBySymbolsListasList(dataAllT_1, symbols))
        res[0] = sum(sum(abs(covMatrx.item((i, j)) - covMatrixT.item((i, j))) for j in range(len(symbols))) for i in range(len(symbols)))
        
        return res
    @staticmethod
    def getCovarianceMatrixBySymbolsListasList(data, symbols):
        # print data
        
        covMatrx = [[0 for i in range(len(symbols))] for i in range(len(symbols))]
        # print covMatrx
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                S1S2covMatrix = StockAnalysis.getCovarianceMatrixByNames(data, symbols[i], symbols[j])
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
        
