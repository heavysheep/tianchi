# coding:utf-8
from pandas import DataFrame
import pandas as pd
import numpy as np
import requests


def date_process(date):
    year, month, day = date.split('-')
    if month[0] == '0':
        month = month[1]
    if day[0] == '0':
        day = day[1]
    return '-'.join([year, month, day])

user_pay_df = pd.read_excel('pay_old.xlsx')
date_list = list(user_pay_df.columns)
for i in range(15):
    day = '%02d' % (i + 1)
    date_list.append('2016-11-' + day)

appkey = 'ba0fb44d48b67f7f1efd48d775ac78f9'
DF = DataFrame()
for date in date_list:
    date_new = date_process(date)
    r = requests.get(url=r'http://japi.juhe.cn/calendar/day', params={
        'date': date_new,
        'key': appkey
    })
    try:
        data = r.json()['result']['data']
    except:
        print(r.text)
        continue
    df = DataFrame([data])
    df.index = [date]
    DF = DF.append(df)
DF.to_excel('calendar.xlsx', encoding='utf-8')

# 在holiday列手工标记了放假安排导致的工作/非工作日情况
# 如果该日为工作日，标记为0
# 如果第二天放假，该日等同于周五计算，标记为1
# 如果改日非工作日，标记为2
DF = pd.read_excel('calendar.xlsx')
DF['holiday'] = DF['holiday'].fillna('N')
for i in range(len(DF['holiday'])):
    if isinstance(DF['holiday'][i], str):
        if DF['weekday'][i] in ['星期六', '星期日']:
            DF['holiday'][i] = 2
        else:
            DF['holiday'][i] = 0
    else:
        continue

for i in range(len(DF['holiday']))[:-1]:
    if DF['holiday'][i + 1] == 2 and DF['holiday'][i] != 2:
        DF['holiday'][i] = 1
DF.to_excel('calendar_process.xlsx')


