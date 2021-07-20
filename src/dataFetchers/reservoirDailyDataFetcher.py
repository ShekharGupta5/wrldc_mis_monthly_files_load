from typing import Dict
import pandas as pd
import datetime as dt
from src.typeDefs.stateConfig import IStateConfig
from src.typeDefs.reservoirMeasRecord import IReservoirDataRecord
from typing import List, Any


def getReservoirDailyData(targetFilePath: str) -> List[List]:

    reservoirDailyRecords: List[IReservoirDataRecord] = []

    dataShtDf = pd.read_excel(
        targetFilePath, sheet_name='SSP Gen 2021-22', header=[0, 1], skipfooter=0)
    # remove 1st column from df
    dataShtDf = dataShtDf.iloc[:, 1:]
    # dataShtDf.columns = ['_'.join(x) for x in dataShtDf.columns]
    dataShtDf = pd.melt(dataShtDf, id_vars=[dataShtDf.columns[0]])
    dataShtDf = dataShtDf.rename(columns={
        dataShtDf.columns[0]: 'data_time', 'variable_0': 'entity_tag',
        'variable_1': 'metric_tag', 'value': 'data_val'})
    # dataShtDf['entity_tag'] = eachRow['name']
    dataShtDf['data_val'].fillna(0, inplace=True)

    # convert dataframe to list of dictionaries
    reservoirDailyRecords = dataShtDf.to_dict('records')

    return reservoirDailyRecords
