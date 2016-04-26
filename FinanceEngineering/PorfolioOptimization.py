import numpy as np
import numpy
from cvxopt import matrix
from cvxopt.solvers import qp, options
from GetData import DataFetcher
from StockAnalysis import StockAnalysis
class PortfolioOptimization(object):
    def __init__(self, params):
        return
    @staticmethod
    def meanVarianceOptimization(data, symbols, r_min, lmbda=0, returnsFromYear=None):
        n = len(symbols)
        returns = StockAnalysis.getReturnsSymbolsList(data, symbols, returnsFromYear)
        P = matrix(StockAnalysis.getCovarianceMatrixBySymbolsListasList(data, symbols)) if lmbda <= 0 else matrix(StockAnalysis.getDynamicCovarianceMatrixBySymbolsListasList(data, symbols, lmbda))
        q = matrix(np.zeros((n, 1)))
        G = matrix(numpy.concatenate((
             np.array([[-x for x in returns]]),
             - numpy.identity(n))))
        h = matrix(numpy.concatenate((
             -numpy.ones((1, 1)) * r_min,
              numpy.zeros((n, 1))), 0))
        r_avg = np.identity(n)
        for i in range(len(returns)):
            r_avg[i][i] = returns[i]
        
        # equality constraint Ax = b; captures the constraint sum(x) == 1
        A = matrix(1.0, (1, n))
        b = matrix(1.0)
        x = np.array([-x for x in returns])
        sol = qp(P, q, G, h, A, b)
        x = np.matrix(sol['x'])
        sol['var'] = x.T * np.matrix(P) * x  
        sol['sigma'] = P 
        sol['returns'] = returns
        sol['return'] = returns * x
        return sol
        
        