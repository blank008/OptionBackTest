import pandas as pd
#
class dataOption(object):
    _data = None

    def __init__(self, df0, df1):
        dataOption._data = self
        self.optiondata = self.dealdate(df0)
        self.etfdata = self.dealdate(df1)

    @classmethod
    def get_instance(cls):
        return dataOption._data

    def getOptionData(self):
        return self.optiondata

    def getEtfData(self):
        return self.etfdata

    def dealdate(self,x):
        listdate = list(x['date'])
        listdate = pd.to_datetime(listdate)
        x['date'] = listdate
        return x