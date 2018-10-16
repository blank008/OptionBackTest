# joinquan平台版权
# 新元blank - 原创 禁止复制商业贩卖 违者必究
# block不可篡改修正记录

'''
参照:
上证50ETF期权合约基本条款
合约标的	上证50交易型开放式指数证券投资基金（“50ETF”）
合约类型	认购期权和认沽期权
合约单位	10000份
合约到期月份	当月、下月及随后两个季月
行权价格	9个（1个平值合约、4个虚值合约、4个实值合约）
行权价格间距	3元或以下为0.05元，3元至5元（含）为0.1元，5元至10元（含）为0.25元，10元至20元（含）为0.5元，20元至50元（含）为1元，50元至100元（含）为2.5元，100元以上为5元
行权方式	到期日行权（欧式）
交割方式	实物交割（业务规则另有规定的除外）
到期日	到期月份的第四个星期三（遇法定节假日顺延）
行权日	同合约到期日，行权指令提交时间为9:15-9:25，9:30-11:30，13:00-15:30
交收日	行权日次一交易日
交易时间	上午9:15-9:25，9:30-11:30（9:15-9:25为开盘集合竞价时间）
下午13:00-15:00（14:57-15:00为收盘集合竞价时间）
委托类型	普通限价委托、市价剩余转限价委托、市价剩余撤销委托、全额即时限价委托、全额即时市价委托以及业务规则规定的其他委托类型
买卖类型	买入开仓、买入平仓、卖出开仓、卖出平仓、备兑开仓、备兑平仓以及业务规则规定的其他买卖类型
最小报价单位	0.0001元
申报单位	1张或其整数倍
涨跌幅限制	认购期权最大涨幅＝max｛合约标的前收盘价×0.5%，min [（2×合约标的前收盘价－行权价格），合约标的前收盘价]×10％｝
认购期权最大跌幅＝合约标的前收盘价×10％
认沽期权最大涨幅＝max｛行权价格×0.5%，min [（2×行权价格－合约标的前收盘价），合约标的前收盘价]×10％｝
认沽期权最大跌幅＝合约标的前收盘价×10％
熔断机制	连续竞价期间，期权合约盘中交易价格较最近参考价格涨跌幅度达到或者超过50%且价格涨跌绝对值达到或者超过5个最小报价单位时，期权合约进入3分钟的集合竞价交易阶段
开仓保证金最低标准	认购期权义务仓开仓保证金＝[合约前结算价+Max（12%×合约标的前收盘价-认购期权虚值，7%×合约标的前收盘价）]×合约单位
认沽期权义务仓开仓保证金＝Min[合约前结算价+Max（12%×合约标的前收盘价-认沽期权虚值，7%×行权价格），行权价格] ×合约单位
维持保证金最低标准	认购期权义务仓维持保证金＝[合约结算价+Max（12%×合约标的收盘价-认购期权虚值，7%×合约标的收盘价）]×合约单位
认沽期权义务仓维持保证金＝Min[合约结算价 +Max（12%×合标的收盘价-认沽期权虚值，7%×行权价格），行权价格]×合约单位
'''

'''
注意事项：
1.暂时忽略行权，具体原因见google，考虑实盘不行权情况
2.日级别数据，分钟、tick暂时数据需要整理清洗，工作量巨大，日后完善
3.集合竞价数据没有，再一个目前集合竞价行情基本没有价格和量
4.研究和回测的黏合性有待研究，所以无法写到研究中，导致代码量可能过长
5.简版的回测，只能做基础研究，业绩归因和复杂回测尚待开发
等
'''

# 导入函数库
from jqdata import *
import pandas as pd
from six import StringIO


# 测试策略为 每个月初买入 远月平值期权的认购、认沽合约 持有5天后平仓策略

def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')

    '''
    设定期权交易手续费和滑点 第一个参数算一张x元、滑点按下单方向的+0.0002 比如买开0.0089 成交价为0.0091 这一单的卖平0.0089 成交价为0.0087
    设定期权交易买入数量限制
    set_OptionOrderCost(OrderCost,Slippage,MaxLimit)
    '''
    # set_OptionOrderCost(2.5,0.0002,0.1)

    df0 = None
    for i in range(4):
        if i == 0:
            # df0 = pd.read_csv((str(2015 + i) + '.csv'),encoding='utf-8-sig')
            df0 = pd.read_csv(StringIO(read_file((str(2015 + i) + '.csv'))), encoding='utf-8-sig')
        else:
            df1 = None
            df1 = pd.read_csv(StringIO(read_file((str(2015 + i) + '.csv'))), encoding='utf-8-sig')
            frames = [df0, df1]
            df0 = pd.concat(frames)
    etfdf0 = pd.read_csv(StringIO(read_file('50etf.csv')), encoding='utf-8')
    dataOption(df0, etfdf0)
    env()


# 每日开盘前运行函数
def before_market_open(context):
    pass


# 每个日bar运行函数
def handle_data(context, data):
    dateday = context.current_dt.day
    datemonth = context.current_dt.month
    dateyear = context.current_dt.year
    if dateday == 1:
        '''
        #近月 远月 季月 下季 4个合约 分认购、认沽 实值、平值、虚值三类
        #调用方式：get_OptionList(month,put,In the Money,date) 
        #第一个参数0,1,2,3分别代表近、远、季、下季 
        #第二个参数0,1代表认购或认沽 
        #第三个参数0,1,2代表实、平、虚
        '''
        optionBuylist = env.get_instance().get_OptionList(0, 0, 0, dat=context.current_dt)

        print(optionBuylist)


# 收盘后运行函数
def after_market_close(context):
    pass


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

    def dealdate(self, x):
        listdate = list(x['date'])
        listdate = pd.to_datetime(listdate)
        x['date'] = listdate
        return x


class OptionApi(object):
    '''
    optionapi所有函数中optionid为期权ID 作为唯一标识 类似股票代码
    '''
    _OptionApi = None

    def __init__(self):
        OptionApi._OptionApi = self
        self.data1 = dataOption.get_instance()
        self.optiondata = self.data1.getOptionData()
        self.etfdata = self.data1.getEtfData()

    @classmethod
    def get_instance(cls):
        return OptionApi._OptionApi

    '''
    history中filed包括：
    open high low close SettlementPrice(成交额) volume(成交量) openinterest(持仓量) uplimit downlimit Delta Gamma Vega Theta Rho
    '''

    def OptionHistory(self, filed, optionid, dt, n):
        return pricelist

    '''
    Bar中filed包括：
    open high low close is_maturity(是否到期) deadlineret(距离到期日还有多少天) SettlementPrice(成交额) volume(成交量) openinterest(持仓量) uplimit downlimit Delta Gamma Vega Theta Rho Volatility(波动率)
    '''

    def OptionBar(self, filed, optionid, dt):
        return price


class env(object):
    _env = None

    def __init__(self):
        env._env = self
        self.data1 = dataOption.get_instance()
        self.optiondata = self.data1.getOptionData()
        self.etfdata = self.data1.getEtfData()
        self.optinPositon = {}
        self.cash = 100000
        self.totalvalue = 100000
        self.marketvalue = 0

    @classmethod
    def get_instance(cls):
        return env._env

    def get_OptionList(self, x1, x2, x3, dat):
        # x1 0 1 2 3 近 远 季 下季
        # x2 0 1 认购 认沽
        # x3 0 1 2 虚值 平值 实值
        # date 时间
        optionlist = []
        date1 = str(dat.date())
        date1 = pd.to_datetime(date1)
        etfprice = list(self.etfdata.loc[self.etfdata.loc[:, 'date'] == date1, :]['close'])[0]

        return etfprice