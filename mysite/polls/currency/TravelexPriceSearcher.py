
from base_searcher import base_searcher
from models import CurrencyRate
import json
import http.client
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time


def getCleanStr(value):
    return value.strip()
def getDateTime(value):
    s=[int(x) for x in value.replace("年","-").replace("月","-").replace("日","").split("-")]
    return datetime(s[0],s[1],s[2])
class TravelexPriceSearcher(base_searcher):
        curencyDic={
                    "USD":1,
                    "AUD":1,
                    "MOP":1,
                    "BRL":1,
                    "DKK":1,
                    "RUB":1,
                    "PHP":1,
                    "HKD":1,
                    "KRW":100,
                    "CAD":1,
                    "NOK":1,
                    "EUR":1,
                    "CNY":1,
                    "JPY":100,
                    "SEK":1,
                    "CHF":1,
                    "TWD":1,
                    "THB":1,
                    "SGD":1,
                    "NZD":1,
                    "IDR":100,
                    "GBP":1
                    }
        
        def getHistoryData(self,currencyCode):
            historyUrl="http://buy.travelex.com.cn/zhcn/RateChart?Profile=online&ProductType=Cash&foreignCurrency=%s" % currencyCode
            data_list=[]
            r=requests.get(historyUrl)
            r=re.search("\(\[\[[\s\S]*\]\]\)",r.text)
            source=r.group().replace("([","").replace("])","")
            source=re.findall("\[[\d]+,[\d|.]+\]",source)
            result=[x.replace("[","").replace("]","").split(",") for x in source]
            for item in result:
                c=CurrencyRate(
                    "Travelex",
                    currencyCode,
                    float(item[1])*(100/TravelexPriceSearcher.curencyDic[currencyCode]),
                    0,
                    datetime.fromtimestamp(int(item[0].replace("00000","00"))))
                print(c)
                data_list.append(c)                   
            return data_list

        def getAllHistoryData(self):
            data_list=[]
            for key in TravelexPriceSearcher.curencyDic:
                data_list.extend(self.getHistoryData(key))
            
            return data_list
            


