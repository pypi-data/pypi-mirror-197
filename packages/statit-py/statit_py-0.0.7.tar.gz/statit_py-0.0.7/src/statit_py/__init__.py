import requests
import multiprocessing
from time import sleep

ENDPOINT = 'https://api.gostatit.com/core'
#ENDPOINT = 'http://localhost:3000/dev/core'
class API:
    """A python API to interact with the api.gostatit.com web API"""
        
    def __init__(self, username: str, apikey: str):
        self.__username = username
        self.__apikey = apikey

    def __post(self, json):
        r = requests.post(ENDPOINT,auth=(self.__username, self.__apikey), json=json)
        if r.status_code != 200 : print(json);raise ValueError(r.text)
        return r.json()
    
    def getCollection(self, id: str) -> dict[str, any]:
        json = {
            'action': 'getCollection', 'input': {
                "id": id,
            },
        }
        return self.__post(json)

    def deleteCollection(self, id: str):
        json = {
            'action': 'deleteCollection', 'input': {
                "id": id,
            },
        }
        self.__post(json)

    def getSerie(self, id: str) -> dict[str, any]:
        json = {
            'action': 'getSerie', 'input': {
                "id": id,
            },
        }
        return self.__post(json)

    def listSeries(self, parentid: str) -> list[dict[str, any]]:
        json = {
            'action': 'listSeries', 'input': {
                "id": parentid,
            },
        }
        return self.__post(json)

    def deleteSerie(self, id: str):
        json = {
            'action': 'deleteSerie', 'input': {
                "id": id,
            },
        }
        self.__post(json)


    def getCollectionJSON(self, input: dict[str, any]) -> dict[str, any]:
        json = {
            'action': 'getCollection', 'input': input,
        }
        return self.__post(json)

    def putCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'putCollection', 'input': input,
        }
        self.__post(json)

    def updateCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'updateCollection', 'input': input,
        }
        self.__post(json)

    def deleteCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'deleteCollection', 'input': input,
        }
        self.__post(json)

    def getSerieJSON(self, input: dict[str, any]) -> dict[str, any]:
        json = {
            'action': 'getSerie', 'input': input,
        }
        return self.__post(json)

    def listSeriesJSON(self, input: dict[str, any]) -> list[dict[str, any]]:
        json = {
            'action': 'listSeries', 'input': input,
        }
        return self.__post(json)
        
    def putSerieJSON(self, input: dict[str, any]):
        json = {
            'action': 'putSerie', 'input': input,
        }
        self.__post(json)

    def batchPutSerieJSON(self, input: list[dict[str, any]]):
        json = {
            'action': 'batchPutSerie', 'input': input,
        }
        self.__post(json)

    def putAllSeriesJSON(self, input: list[dict[str, any]]):
        batch = []
        i=0
        for serie in input:
            print(str(i*100//len(input)) + '%')
            i+=1
            batch.append(serie)
            if len(batch) == 25:
                self.batchPutSerieJSON(batch)
                batch = []
        if batch != [] : self.batchPutSerieJSON(batch)
        
    def updateSerieJSON(self, input: dict[str, any]):
        json = {
            'action': 'updateSerie', 'input': input,
        }
        self.__post(json)

    def deleteSerieJSON(self, input: dict[str, any]):
        json = {
            'action': 'deleteSerie', 'input': input,
        }
        self.__post(json)
    



    

