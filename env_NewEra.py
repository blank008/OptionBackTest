# -*- coding: utf-8 -*-
from data_NewEra import dataOption
import pandas as pd
#
class env(object):
    _env = None

    def __init__(self):
        env._env = self
        self.data = dataOption.get_instance()
        self.optiondata = self.data.getOptionData()
        self.etfdata = self.data.getEtfData()
        self.optinPositon = {}

    @classmethod
    def get_instance(cls):
        return env._env

    def get_OptionList(self, x1, x2, x3, dat):
        # x1 0 1 2 3 近 远 季 下季
        # x2 1 -1 认购 认沽
        # x3 0 1 2 虚值 平值 实值
        # date 时间
        optionlist = []
        time1 = pd.to_datetime(dat)
        etfprice = list(self.etfdata.loc[self.etfdata.loc[:,'date']==time1,:]['close'])[0]
        CurrentYear = time1.date().year
        CurrentMonth = time1.date().month
        CurrentDay = time1.date().day

        AllODf = self.optiondata.loc[self.optiondata.loc[:,'date']==time1,:]

        if x3 == 1: #平值
            AllODf = AllODf[AllODf.optionK <= etfprice+0.1]
            AllODf = AllODf[AllODf.optionK >= etfprice-0.1]
        if x3 == 0: #虚值
            if x2 == 1: #认购
                AllODf = AllODf[ (etfprice + 0.1) < AllODf.optionK ]
            if x2 == -1: #认沽
                AllODf = AllODf[ (etfprice - 0.1) > AllODf.optionK ]

        if x3 == 2: #实值
            if x2 == 1: #认购
                print(etfprice)
                AllODf = AllODf[ (etfprice + 0.1) > AllODf.optionK ]
            if x2 == -1: #认沽
                AllODf = AllODf[ (etfprice - 0.1) < AllODf.optionK ]

        AllODf1 = AllODf[['optionID', 'optionName']]
        if x2 == 1: #认购
            optionidlist = []
            optionName1 = list(AllODf1['optionName'])
            optionID1 = list(AllODf1['optionID'])
            for i in range(len(optionID1)):
                year2 = 0
                year2 = self.findOptionYear(optionName1[i])
                if self.findPutOpT(year2,optionName1[i]) == str('购'):
                    optionidlist.append(optionID1[i])
            AllODf = AllODf.loc[AllODf['optionID'].isin(optionidlist)]

        else: #认沽
            optionidlist = []
            optionName1 = list(AllODf1['optionName'])
            optionID1 = list(AllODf1['optionID'])
            for i in range(len(optionID1)):
                year2 = 0
                year2 = self.findOptionYear(optionName1[i])
                if self.findPutOpT(year2,optionName1[i]) != str('购'):
                    optionidlist.append(optionID1[i])
            AllODf = AllODf.loc[AllODf['optionID'].isin(optionidlist)]

        AllODf2 = AllODf[['optionID','optionName']]
        optionName2 = list(AllODf2['optionName'])
        optionID2 = list(AllODf2['optionID'])

        mon1 = self.moncalu(CurrentMonth,x1)

        AllODf = self.findOpT(AllODf2, AllODf, mon1, optionName2, optionID2)

        return AllODf

    def findOptionMonth(self,OpT):
        a = OpT
        a = str(a)
        b = a.split('年')[1]
        b = b.split('月')[0]
        return int(b)
    def findOptionYear(self,OpT):
        a = OpT
        a = str(a)
        if str('购') in a:
            b = a.split('购')[1]
            b = b.split('年')[0]
        if str('沽') in a:
            b = a.split('沽')[1]
            b = b.split('年')[0]
        return int(b)
    def findPutOpT(self,year1,OpT):
        a = OpT
        a = str(a)
        b = a.split('ETF')[1]
        b = b.split(str(year1))[0]
        return b
    def findOpT(self,AllODf2,AllODf,mon,optionName2,optionID2):
        optionidlist2 = []
        for j in range(len(optionName2)):
            monthopt = 0
            monthopt = self.findOptionMonth(optionName2[j])
            if monthopt == mon:
                optionidlist2.append(optionID2[j])
        AllODf = AllODf.loc[AllODf['optionID'].isin(optionidlist2)]
        return AllODf
    def moncalu(self,monthnow,x):
        monthR = 0
        #X 0 1 2 3
        monlist = [3,6,9,12]
        if x == 0:
            monthR = monthnow
        if x == 1:
            monthR = monthnow + 1
        if x == 2:
            if monthnow in monlist:
                for k in range(len(monlist)):
                    if monthnow == monlist[k]:
                        if k != 3:
                            monthR = monlist[k+1]
                        if k == 3:
                            monthr = monlist[0]
            else:
                getN = 0
                for k in range(len(monlist)):
                    if getN == 0:
                        if monthnow < monlist[k]:
                            monthR = monlist[k+1]
                            getN = 1

        if x == 3:
            if monthnow in monlist:
                for k in range(len(monlist)):
                    if monthnow == monlist[k]:
                        if k != 2:
                            monthR = monlist[k+2]
                        if k == 2:
                            monthr = monlist[3]
            else:
                getN = 0
                for k in range(len(monlist)):
                    if getN == 0:
                        if monthnow < monlist[k]:
                            monthR = monlist[k+2]
                            getN = 1
        return monthR
