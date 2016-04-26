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
    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def GetCompaniesHistoryDataToFiles(companiesFile, startDate, endDate, outputFolder):
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
    def GetCompaniesHistoryDataToDict(companiesFile, startDate, endDate):
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
    def GetCompaniesReturnsFromHistFilesDirPath(histFilesDirPath, dateIdx=0, closePriceIdx=1,outputReturnFile=""):
        histFilesDirPath = histFilesDirPath.replace(r'\\', os.sep)
        retDict = {}
        symbols = []
        files = [f for f in listdir(histFilesDirPath) if isfile(join(histFilesDirPath, f))]
        for fileName in sorted(files):
            symbol = fileName.replace(".csv", "")
            symbols.append(symbol)
            filePath = join(histFilesDirPath, fileName)
            with open(filePath, 'rb') as file:
                reader = csv.reader(file)
                data = [[line[dateIdx], line[closePriceIdx]] for line in reader][1:]
                for i in range(len(data) - 1):
                    date = data[i][0]
                    dateParts = date.split("/") if "/" in date else date.split("-")
                    dateParts = reversed(dateParts) if len(dateParts[-1]) == 4 else dateParts
                    date = "-".join(dateParts)
                    ret = math.log(float(data[i][1]) / float(data[i + 1][1]))
                    if date not in retDict:
                        retDict[date] = {}
                    retDict[date][symbol] = ret
        return retDict, symbols
                
                    
    @staticmethod
    def GetCompaniesYieldsToDictWriteOutput(companiesFile, startDate, endDate, outputFile = ""):
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
    def GetCompaniesReturnsToDict(companiesFile, startDate, endDate,outputFile = ""):
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
        if outputFile:
            with open (outputFile, "wb") as file:
                writer = csv.writer(file)
                writer.writerow(["date"] + [symbolIdx[i][0] for i in range(len(symbolIdx))])
                for date in sorted(retDict.keys(), key=lambda d: map(int, d.split('-'))):
                    writer.writerow([date] + [retDict[date][symbolIdx[i][0]] if symbolIdx[i][0] in retDict[date] else "" for i in range(len(symbolIdx))])    
            
        print symbolIdx
        return retDict, symbols
