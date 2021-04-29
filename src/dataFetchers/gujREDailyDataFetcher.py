from typing import Dict
import pandas as pd
import datetime as dt
from src.typeDefs.measRecord import IMetricsDataRecord
from typing import List, Any


def getGujREGenerationData(targetFilePath: str) -> List[List[IMetricsDataRecord]]:
    allGujRERecords: List[List[IMetricsDataRecord]] = []
    gujREGenerationDailyRecords: List[IMetricsDataRecord] = []

    excelWorkBook = pd.ExcelFile(targetFilePath)
    gujREGenerationSheets = excelWorkBook.sheet_names

    for eachDaySheet in gujREGenerationSheets:
        df = pd.read_excel(
            targetFilePath, sheet_name=eachDaySheet, nrows=1, header=None)
        dateCells = [x for x in df.iloc[0, :] if isinstance(x, dt.datetime)]
        if len(dateCells) == 0:
            continue
        dataShtDf = pd.read_excel(
            targetFilePath, sheet_name=eachDaySheet, skiprows=1)
        if dataShtDf.shape[0] > 24:
            dataShtDf = dataShtDf.iloc[0:24, :]
        newCols = [x for x in dataShtDf.columns if not (
            x.startswith('Unnamed') or x.isspace())]
        dataShtDf = dataShtDf[newCols]
        dataShtDf['Date'] = dateCells[0]
        dataShtDf['Date'] += pd.to_timedelta(dataShtDf.Hours, unit='h')
        del dataShtDf['Hours']
        dataShtDf.columns = [' '.join(x.split()) for x in dataShtDf.columns]
        dataShtDf = dataShtDf.rename(columns={
            dataShtDf.columns[1]:'Solar(MW)',
            dataShtDf.columns[0]:'Wind(MW)'
        })
        dataShtDf = pd.melt(dataShtDf, id_vars=['Date'])
        dataShtDf['entity_tag'] = 'gujrat'
        dataShtDf = dataShtDf.rename(columns={
            dataShtDf.columns[0]: 'data_time', 'variable': 'metric_name',
            'value': 'data_val'})
        gujREGenerationDailyRecords = dataShtDf.to_dict('records')
        allGujRERecords.append(gujREGenerationDailyRecords)
    return allGujRERecords
