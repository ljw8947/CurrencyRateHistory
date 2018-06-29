
from base_searcher import base_searcher
from models import CurrencyRate
import json
import http.client
import requests
import re
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import time

class BOCPriceSearcher(base_searcher):
        curencyDic={
                    "GBP":{"num":"1314","name":"英镑"},
                    "HKD":{"num":"1315","name":"港币"},
                    "USD":{"num":"1316","name":"美元"},
                    "SGD":{"num":"1375","name":"新加坡元"},
                    "SEK":{"num":"1320","name":"瑞典克朗"},
                    "DKK":{"num":"1321","name":"丹麦克朗"},
                    "NOK":{"num":"1322","name":"挪威克朗"},
                    "JPY":{"num":"1323","name":"日元"},
                    "CAD":{"num":"1324","name":"加拿大元"},
                    "AUD":{"num":"1325","name":"澳大利亚元"},
                    "EUR":{"num":"1326","name":"欧元"},
                    "MOP":{"num":"1327","name":"澳门元"},
                    "PHP":{"num":"1328","name":"菲律宾比索"},
                    "THB":{"num":"1329","name":"泰国铢"},
                    "NZD":{"num":"1330","name":"新西兰元"},
                    "KRW":{"num":"1331","name":"韩元"},
                    "RUB":{"num":"1843","name":"卢布"},
                    "MYR":{"num":"2890","name":"林吉特"},
                    "TWD":{"num":"2895","name":"新台币"},
                    "IDR":{"num":"3030","name":"印尼卢比"},
                    "BRL":{"num":"3253","name":"巴西里亚尔"},
                    "AED":{"num":"3899","name":"阿联酋迪拉姆"},
                    "INR":{"num":"3900","name":"印度卢比"},
                    "ZAR":{"num":"3901","name":"南非兰特"},
                    "SAR":{"num":"4418","name":"沙特里亚尔"},
                    "TRY":{"num":"4560","name":"土耳其里拉"}
                }

        
        def getHistoryData(self,currencyCode):
            historyUrl="http://srh.bankofchina.com/search/whpj/search.jsp"
            data_list=[]
            date=datetime(2016,1,1).date()
            while date<datetime.today().date():
                r=requests.post(historyUrl,data={"erectDate":str(date),
                    "nothing":str(date),
                    "pjname":BOCPriceSearcher.curencyDic[currencyCode]["num"]})
                soup=BeautifulSoup(r.text,'html5lib')
                soup=soup.find_all("table")[1]
                tds=soup.find_all("tr")[1].find_all("td")
                data=CurrencyRate(
                    "BOC",
                    currencyCode,
                    tds[4].contents[0] if len(tds[4].contents) != 0 else 0,
                    tds[2].contents[0] if len(tds[2].contents) != 0 else 0,
                    datetime.strptime(tds[7].contents[0],"%Y.%m.%d %H:%M:%S").date()
                )
                print(str(data))
                data_list.append(data)
                date=date+timedelta(days=1)
            return data_list

        def getAllHistoryData(self):
            data_list=[]
            for key in BOCPriceSearcher.curencyDic.keys():
                data_list.extend(self.getHistoryData(key))
            return data_list
            


