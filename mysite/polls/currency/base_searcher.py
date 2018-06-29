class base_searcher(object):
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self,value):
        self._url=value
    
    '''返回解析的数据'''
    def getData(self):
        pass
    

