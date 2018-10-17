import pandas as pd
df0 = pd.read_csv(('2018.csv'),encoding='utf-8-sig')

listname = list(df0['optionName'])
listnamenew = []
for Oname in listname:
    a = str(Oname)
    if str('年') not in a:
        if str('购') in a: #认购后加2018年
            b = a.split('购')[0]
            b1 = a.split('购')[1]
            a = str(b)+'购'+'2018年'+str(b1)
        else: #认沽后加2018年
            b = a.split('沽')[0]
            b1 = a.split('沽')[1]
            a = str(b)+'沽'+'2018年'+str(b1)
        listnamenew.append(a)
    else:
        listnamenew.append(a)

df0['optionName'] = listnamenew
df0.to_csv('2018_new.csv')

# print(df0)

# a = '50ETF沽2016年3月2.65A'
# a = str(a)
# if str('A') in a:
#     a=a.strip('A')
#     print(a)
# if str('购') in a:
#     b = a.split('购')[1]
#     b = b.split('年')[0]
#     print(b)
# if str('沽') in a:
#     b = a.split('沽')[1]
#     b = b.split('年')[0]
#     print((b))
