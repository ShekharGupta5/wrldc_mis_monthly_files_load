from src.config.appConfig import initConfigs , getJsonConfig
from src.config.appConfig import getStateConfigs, getFileMappings
from src.app.statesHourlyService import statesHourlyService
from src.app.statesDailyService import statesDailyService
from src.app.freqDailyService import freqDailyService
from src.dataFetchers.dataFetcherHandler import getExcelFilePath
from src.app.linesGenService import linesGenService
from src.app.voltDailyService import voltDailyService
from src.app.reservoirService import reservoirService
from src.app.gujREGenerationService import gujREGenerationService
from src.utils.addMonths import addMonths
import datetime as dt
import cx_Oracle

initConfigs()
appConfig = getJsonConfig()

cxOraclePath = appConfig['cxOraclePath']
if not cxOraclePath == '':
    cx_Oracle.init_oracle_client(lib_dir= cxOraclePath)

filesSheet = getFileMappings()
statesConfigSheet = getStateConfigs()

startMonth = dt.datetime(2021, 3, 1)
endMonth = dt.datetime(2021, 3, 31)

targetMonth = startMonth
while targetMonth <= endMonth:
    print('processing for {0}'.format(targetMonth))
    for eachrow in filesSheet:
        print(eachrow['file_type'])
        excelFilePath = getExcelFilePath(eachrow, targetMonth)
        if eachrow['file_type'] == 'state_hourly_data':
            statesHourlyService(statesConfigSheet, excelFilePath)
        # if eachrow['file_type'] == 'state_daily_data':
        #     statesDailyService(statesConfigSheet, excelFilePath)
        # if eachrow['file_type'] == 'gen_lines_daily_data':
        #     linesGenService(statesConfigSheet, excelFilePath)
        # if eachrow['file_type'] == 'freq_vol_data':
        #     freqDailyService(excelFilePath)
        #     voltDailyService(excelFilePath)
        # if eachrow['file_type'] == 'reservoir_data':
        #     reservoirService(excelFilePath)
        # if eachrow['file_type'] == 'guj_RE_gen_daily_data':
        #     excelFilePath = getExcelFilePath(eachrow, targetMonth)
        #     gujREGenerationService(excelFilePath)
    targetMonth = addMonths(targetMonth, 1)
