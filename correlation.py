#!/bin/python3
import pandas as pd
import statistics as stat
import numpy as np
import sys
import argparse


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

def readSheetData(excelFile, sheet):
    df = pd.read_excel(excelFile, sheet)
    return pd.DataFrame(df, columns = [DATE_COLUMN, PRICE_COLUMN])

def main(argv):
    optParser = argparse.ArgumentParser(description = 'Indexes correlation calculator')
    optParser.add_argument('-i', '--inputFile')
    args = optParser.parse_args(argv)

    data = loadFile(args.inputFile)
    normalizedData = normalizeData(data)
    cols = len(normalizedData.columns)

    print(normalizedData)
    arrs = []

    for n in range(cols):
        if n == 0:
            continue
        arrs.append(normalizedData.iloc[:, n].array)
    corrCoef = np.corrcoef(arrs)
    print(corrCoef)




if __name__ == "__main__":
    main(sys.argv[1:])
