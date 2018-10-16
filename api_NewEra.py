"""
相关api介绍


"""
from data_NewEra import dataOption


#
class OptionApi(object):
    _OptionApi = None

    def __init__(self):
        OptionApi._OptionApi = self
        self.data = dataOption.get_instance()
        self.optiondata = self.data.getOptionData()
        self.etfdata = self.data.getEtfData()

    @classmethod
    def get_instance(cls):
        return OptionApi._OptionApi


