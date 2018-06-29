
from CMBPriceSearcher import CMBPriceSearcher
from BOCPriceSearcher import BOCPriceSearcher
from TravelexPriceSearcher import TravelexPriceSearcher

#travelex get data
travelexSearcher=TravelexPriceSearcher()
travelexData=travelexSearcher.getAllHistoryData()
for item in travelexData:
    item.save()


#boc get data
bocSearch= BOCPriceSearcher()
bocData=bocSearch.getAllHistoryData()
for item in bocData:
    item.save()

#cmb get data
cmbSearcher=CMBPriceSearcher()
cmbData=cmbSearcher.getAllHistoryData()
for item in cmbData:
    item.save()