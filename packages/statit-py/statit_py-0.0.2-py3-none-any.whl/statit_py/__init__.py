import requests
from typing import Callable

ENDPOINT = 'https://api.gostatit.com/core'
class API:
    """An API to interact with the api.gostatit.com web API"""
        
    def __init__(self, username: str, apikey: str):
        self.__username = username
        self.__apikey = apikey

    def __post(self, json):
        r = requests.post(ENDPOINT,auth=(self.__username, self.__apikey), json=json)
        if r.status_code != 200 : raise ValueError(r.text)
        return r.json()
    
    def getCollection(self, id: str) -> dict[str, any]:
        json = {
            'action': 'getCollection', input: {
                "id": id,
            },
        }
        return self.__post(json)

    def deleteCollection(self, id: str):
        json = {
            'action': 'deleteCollection', input: {
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

    def listSeries(self, id: str) -> list[dict[str, any]]:
        json = {
            'action': 'listSerie', 'input': {
                "id": id,
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
            'action': 'getCollection', input: input,
        }
        return self.__post(json)

    def putCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'putCollection', input: input,
        }
        self.__post(json)

    def updateCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'updateCollection', input: input,
        }
        self.__post(json)

    def deleteCollectionJSON(self, input: dict[str, any]):
        json = {
            'action': 'deleteCollection', input: input,
        }
        self.__post(json)

    def getSerieJSON(self, input: dict[str, any]) -> dict[str, any]:
        json = {
            'action': 'getSerie', 'input': input,
        }
        return self.__post(json)

    def listSeriesJSON(self, input: dict[str, any]) -> list[dict[str, any]]:
        json = {
            'action': 'listSerie', 'input': input,
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

def observationalise(table: list[list], line_to_date: Callable[[list], int | None], line_to_value: Callable[[list], int | None], line_to_key: Callable[[list], str | None]) -> dict[str, list[str, int | float]]:
     """
     Takes a list of lines and aranges them into series

     Arguments
     ----------
          table : list(list)
               A list of lines (an line is line in a CSV file)
          line_to_date : (list) -> int | None
               A function whose input is an line and output is the corresponding date, if there exists one
          line_to_value : (list) -> int | None
               A function whose input is an line and output is the corresponding value, if there exists one
          line_to_key : (list) -> str | None
               A function whose input is an line and output is the corresponding key of the serie, if there exists one
     
     Out
     ---
     A dictionary whose keys are the keys of lines anf values are a list of observations

     """
     CHARS = '#####'
     key_datified = {
        line_to_key(line)+CHARS+line_to_date(line)+CHARS+str(i) : (line_to_value(line)) 
        for line,i in zip(table,range(len(table)))
        if line_to_date(line) and line_to_key(line)

     }
     aggregated = {}
     for key, value in key_datified.items():
            k=(key.split(CHARS)); k=k[0]+CHARS+k[1]
            try:
                aggregated[k] += value
            except(KeyError):
               aggregated[k] = value
            except(TypeError):
                pass
              
     out = {}
     for key,value in aggregated.items():
          k = key.split(CHARS)
          try:   
               out[k[0]].append((k[1], value))
          except(KeyError):
               out[k[0]] = [(k[1], value)]
     return out
    
    

