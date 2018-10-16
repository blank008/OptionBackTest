# import pandas as pd
# df0 = pd.read_csv(('2015.csv'),encoding='utf-8')
# print(df0)

a = '50ETF沽2016年3月2.65A'
a = str(a)
if str('A') in a:
    a=a.strip('A')
    print(a)
if str('购') in a:
    b = a.split('购')[1]
    b = b.split('年')[0]
    print(b)
if str('沽') in a:
    b = a.split('沽')[1]
    b = b.split('年')[0]
    print((b))
