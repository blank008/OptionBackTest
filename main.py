# 导入函数库
from env_NewEra import *
# from main_NewEra import *
# from result_NewEra import *
from data_NewEra import *
from api_NewEra import *

import pandas as pd
# from six import StringIO

# 测试策略为 每个月初买入 远月平值期权的认购、认沽合约 持有5天后平仓策略

# 近月 远月 季月 下季 4个合约 分认购、认沽 实值、平值、虚值三类
# 调用方式：get_OptionList(month,put,In the Money,date)
# 第一个参数0,1,2,3分别代表近、远、季、下季
# 第二个参数0,1代表认购或认沽
# 第三个参数0,1,2代表实、平、虚

# def initialize(context):
    # 设定沪深300作为基准
    # set_benchmark('000300.XSHG')
    # 设定期权交易手续费和滑点 第一个参数算一张x元、滑点按下单方向的+0.0002 比如买开0.0089 成交价为0.0091 这一单的卖平0.0089 成交价为0.0087
    # set_OptionOrderCost(2.5,0.0002)

    #
df0 = None
for i in range(4):
    if i == 0 :
        df0 = pd.read_csv((str(2015 + i) + '.csv'),encoding='utf-8-sig')
    else:
        df1 = None
        df1 = pd.read_csv((str(2015 + i) + '.csv'),encoding='utf-8-sig')
        frames = [df0, df1]
        df0 = pd.concat(frames)
etfdf0 = pd.read_csv('50etf.csv',encoding='utf-8')
dataOption(df0, etfdf0)
env()
# 每日开盘前运行函数
# def before_market_open(context):
date1 = '2015/03/13'
optionBuylist = env.get_instance().get_OptionList(2, 1, 2, dat=date1)
print(optionBuylist)
    # pass


# 每个日bar运行函数
def handle_data(context, data):
    dateday = context.current_dt.day
    datemonth = context.current_dt.month
    dateyear = context.current_dt.year

    # print(dateyear)
    # if dateday == 1:
    #     optiondf = env.get_instance()
    #     print(optiondf.etfdata)


# 收盘后运行函数
def after_market_close(context):
    pass

