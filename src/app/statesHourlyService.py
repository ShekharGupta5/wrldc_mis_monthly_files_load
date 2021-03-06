from src.config.appConfig import getJsonConfig
from src.dataFetchers.dataFetcherHandler import statesHourlyDataFetcherHandler
from src.typeDefs.stateConfig import IStateConfig
from src.repos.measData.measDataRepo import MeasDataRepo
from typing import List


def statesHourlyService(stateConfigSheet: List[IStateConfig], excelFilePath):
    stateHourlyRecords = statesHourlyDataFetcherHandler(
        stateConfigSheet, excelFilePath)
    measDataRepo = MeasDataRepo(getJsonConfig()['appDbConnStr'])

    for each in stateHourlyRecords:
        isRawCreationSuccess = measDataRepo.insertStatesHourlyData(each)
        if isRawCreationSuccess:
            print("State Hourly data insertion SUCCESSFUL for {0}".format(
                each[0]['entity_tag']))
        else:
            print("State Hourly data insertion UNSUCCESSFUL for {0}".format(
                each[0]['entity_tag']))
