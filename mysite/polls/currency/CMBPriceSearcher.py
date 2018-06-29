
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
class CMBPriceSearcher(base_searcher):
        curencyDic={
                    "美元":"USD",
                    "日元":"JPY",
                    "欧元":"EUR",
                    "港币":"HKD",
                    "新加坡元":"SGD",
                    "澳大利亚元":"AUD",
                    "英镑":"GBP",
                    "加拿大元":"CAD",
                    "瑞士法郎":"CHF",
                    "新西兰元":"NZD"
                }

        
        def getData(self):
            r=requests.get("http://fx.cmbchina.com/hq/")
            r=re.search('[\s]{1}<table cellpadding="0" cellspacing="1" width="740" align="center" class="data">[\s\S]*</table>[\s]{1}',r.text)
            soup=BeautifulSoup(r.group(),'html5lib')
            data_list=[]
            for idx,tr in enumerate(soup.find_all("tr")):
                if idx!=0:
                    tds=tr.find_all("td")
                    data_list.append(CurrencyRate(
                        "CMB",
                        CMBPriceSearcher.curencyDic[getCleanStr(tds[0].contents[0])],
                        getCleanStr(tds[4].contents[0]),
                        getCleanStr(tds[6].contents[0])))
            return data_list
        
        def getHistoryData(self,currencyCHNName):
            historyUrl="http://fx.cmbchina.com/Hq/History.aspx?&nbr=%s&page=" % currencyCHNName
            data_list=[]
            for pageID in range(1,20):
                r=requests.get(historyUrl+str(pageID))
                r=re.search('</tbody>[\s]+<tbody>[\s\S]*</tr>[\s]+</tbody>',r.text)
                soup=BeautifulSoup("<table>"+r.group()+"</table>",'html5lib')
                
                for tr in soup.find_all("tr"):
                    tds=tr.find_all("td")
                    data_list.append(CurrencyRate(
                        "CMB",
                        CMBPriceSearcher.curencyDic[currencyCHNName],
                        getCleanStr(tds[4].contents[0]),
                        getCleanStr(tds[2].contents[0]),
                        getDateTime(getCleanStr(tds[0].contents[0]))))
                    
                time.sleep(1)
            return data_list

        def getAllHistoryData(self):
            data_list=[]
            for key in CMBPriceSearcher.curencyDic.keys():
                data_list.extend(self.getHistoryData(key))
            
            return data_list
            


