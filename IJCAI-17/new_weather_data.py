# coding:utf-8
from pandas import DataFrame
import pandas as pd
import numpy as np
import gc

df_pay = pd.read_excel(r'pay_new_3.xlsx')
date_array = np.unique(df_pay['day'])
city_array = np.unique(df_pay['city_name'])


spell_df = pd.read_table('pinyin.txt', sep='    ', encoding='utf-8', engine='python')
DF = DataFrame()
for city in city_array:
    city_spell = spell_df['中文'][city]
    weather_path = r'city_weather\%s' % city_spell
    weather_table = pd.read_table(weather_path, sep=',', header=None, encoding='utf-8')
    weather_table.columns = ['time', 'high', 'low', 'weather', 'wind', 'wind_level']
    weather_table = weather_table[['time', 'high', 'low', 'weather']]
    weather_table['city'] = city
    weather_table.set_index('city', drop=True, inplace=True)
    DF = DF.append(weather_table)
    gc.collect()
DF.to_excel(r'weather_data.xlsx')
