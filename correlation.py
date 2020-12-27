#!/bin/python3
import pandas as pd
import statistics as stat
import numpy as np
import sys
import argparse
import datetime


DATE_COLUMN = 'Date'
PRICE_COLUMN = 'Price'

def loadFile(dataFile):
    xlsx = pd.ExcelFile(dataFile, engine='openpyxl')
    sheets = xlsx.sheet_names
    data = []
    for sheet in sheets:
        sheetData = readSheetData(xlsx, sheet)
        data.append(sheetData)
    return data

def normalizeData(data):
    dd = None
    for n in range(len(data)):
        if n== 0:
            dd = pd.merge(data[n], data[n+1], how = 'inner', on = [DATE_COLUMN])
        elif n < len(data) - 1:
            dd = pd.merge(dd, data[n+1], how = 'inner', on = [DATE_COLUMN])
    return dd

def sliceData(data, year):
    dateBeginning = datetime.date(year, 1, 1)
    dateEnding = datetime.date(year, 12, 31)
    return data[(data[DATE_COLUMN] >= np.datetime64(dateBeginning)) & (data[DATE_COLUMN] <= np.datetime64(dateEnding))]

def readSheetData(excelFile, sheet):
    df = pd.read_excel(excelFile, sheet)
    return pd.DataFrame(df, columns = [DATE_COLUMN, PRICE_COLUMN])

def calculateCorrelation(normalizedData):
    cols = len(normalizedData.columns)

    print('Data for calculation')
    print(normalizedData)
    arrs = []

    for n in range(cols):
        if n == 0:
            continue
        arrs.append(normalizedData.iloc[:, n].array)
    corrCoef = np.corrcoef(arrs)
    print(corrCoef)
    print('\n\n\n')

def main(argv):
    optParser = argparse.ArgumentParser(description = 'Indexes correlation calculator')
    optParser.add_argument('-i', '--inputFile')
    args = optParser.parse_args(argv)

    data = loadFile(args.inputFile)
    normalizedData = normalizeData(data)
    print('Overall')
    calculateCorrelation(normalizedData)

    print('Yearly data')
    for year in range(2015, 2021):
        print(year)
        slicedData = sliceData(normalizedData, year)
        calculateCorrelation(slicedData)




if __name__ == "__main__":
    main(sys.argv[1:])
