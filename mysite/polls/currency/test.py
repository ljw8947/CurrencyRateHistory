from CtripPriceSearcher import CtripPriceSearcher
searcher=CtripPriceSearcher()
data=searcher.getData()
for item in data:
    print(item)