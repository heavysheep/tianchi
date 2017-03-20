# coding:utf-8
from pandas import DataFrame
import pandas as pd
import numpy as np
import gc

class get_data():
    def build_user_pay(self):
        # 生成支付  店铺-日期数据
        user_pay_df = pd.read_table(r'C:\Users\prince\Desktop\dataset\dataset\user_pay.txt', sep=',', header=None, encoding='utf-8')
        user_pay_df.columns = ['user_id', 'shop_id', 'time_stamp']
        user_pay_df['day'] = user_pay_df['time_stamp'].apply(lambda date: date.split(' ')[0])
        user_pay_df['time'] = user_pay_df['time_stamp'].apply(lambda date: date.split(' ')[1])
        user_pay_df.set_index('shop_id', drop=True, inplace=True)
        user_pay_se = user_pay_df['day']
        df_pay = DataFrame()
        count = 0
        for shop_id in np.unique(user_pay_df.index):
            shop_se = user_pay_se[shop_id]
            shop_count = shop_se.value_counts()
            shop_count = shop_count[shop_count.notnull()]
            shop_df = DataFrame(shop_count)
            shop_df['shop_id'] = shop_id
            df_pay = df_pay.append(shop_df)
            count += 1
            print(count)
            gc.collect()
        df_pay.reset_index(inplace=True)
        df_pay.rename(columns={'day': 'result', 'index': 'day'}, inplace=True)
        df_pay = df_pay.sort_values(by=['shop_id', 'day'])
        df_pay.reset_index(inplace=True, drop=True)
        df_pay.to_excel('pay_new.xlsx', encoding='utf-8')

    def add_test_data(self):
        # 构筑测试集
        df_pay = pd.read_excel(r'pay_new.xlsx', encoding='utf-8')
        df_test = DataFrame()
        df_calendar = pd.read_excel(r'calendar_process.xlsx', encoding='utf-8')
        test_index = df_calendar.loc['2016-11-01': '2016-11-14'].index
        for shop_id in range(1, 2001):
            df = DataFrame(test_index, columns=['day'])
            df['shop_id'] = shop_id
            df_test = df_test.append(df)
        df_test['result'] = -1
        df_pay = df_pay.append(df_test)
        df_pay.reset_index(inplace=True, drop=True)
        df_pay.to_excel('pay_new.xlsx', encoding='utf-8')
        # train: [0:599274]  test: [599275: 627274]

    def build_shop_feature(self):
        # 添加店铺特征
        df_shop_info = pd.read_excel(r'C:\Users\prince\Desktop\dataset\dataset\shop_info.xlsx', encoding='utf-8')
        df_shop_info.set_index('shop_id', inplace=True)
        df_shop_info['tag_3'] = df_shop_info.apply(lambda x:x['cate_3_name'] if isinstance(x['cate_3_name'], str) else x['cate_2_name'], axis=1)
        df_shop_info['tag_2'] = df_shop_info.apply(lambda x:x['cate_2_name'] if isinstance(x['cate_2_name'], str) else x['cate_1_name'], axis=1)
        df_shop_info.rename(columns={'cate_1_name': 'tag_1'}, inplace=True)
        df_shop_info.drop(['location_id', 'cate_2_name', 'cate_3_name'], axis=1, inplace=True)
        df_pay = pd.read_excel('pay_new.xlsx', encoding='utf-8')
        print(df_pay)
        df_pay = pd.merge(df_shop_info, df_pay, left_index=True, right_on='shop_id')
        df_pay.to_excel('pay_new_2.xlsx', encoding='utf-8')

    def holiday_data(self):
        # 添加节假日特征
        # need cal.py result
        df_calendar = pd.read_excel('calendar_process.xlsx', encoding='utf-8')
        df_holiday = DataFrame(df_calendar['holiday'])

        df_pay = pd.read_excel(r'pay_new_2.xlsx')
        df_pay = pd.merge(df_pay, df_holiday, left_on='day', right_index=True)
        df_pay.sort_index(inplace=True)
        df_pay.to_excel('pay_new_3.xlsx', encoding='utf-8')

    def build_weather_data(self):
        # 生成天气数据表
        df_pay = pd.read_excel(r'pay_new_3.xlsx')
        date_array = np.unique(df_pay['day'])
        city_array = np.unique(df_pay['city_name'])
        spell_df = pd.read_table('pinyin.txt', sep='    ', encoding='utf-8', engine='python')
        DF = DataFrame()
        for city in city_array:
            city_spell = spell_df['中文'][city]
            weather_path = r'city_weather\%s' % city_spell
            weather_table = pd.read_table(weather_path, sep=',', header=None, encoding='utf-8')
            weather_table.columns = ['day', 'high', 'low', 'weather', 'wind', 'wind_level']
            weather_table = weather_table[['time', 'high', 'low', 'weather']]
            weather_table['city_name'] = city
            weather_table.set_index('city', drop=True, inplace=True)
            DF = DF.append(weather_table)
            gc.collect()
        DF.to_excel(r'weather_data.xlsx', encoding='utf-8')

    def add_weather(self):
        # 添加天气特征
        weather_df = pd.read_excel(r'weather_data.xlsx', encoding='utf-8')
        df_pay = pd.read_excel(r'pay_new_3.xlsx', encoding='utf-8')
        df_pay = pd.merge(df_pay, weather_df, how='left')
        df_pay.to_excel('pay_new_4.xlsx', encoding='utf-8')

    def build_view_data(self):
        # 生成浏览  店铺-日期数据
        user_view_df = pd.read_table(r'C:\Users\prince\Desktop\dataset\dataset\user_view.txt', sep=',', header=None, encoding='utf-8')
        user_view_df.columns = ['user_id', 'shop_id', 'time_stamp']
        user_view_df['day'] = user_view_df['time_stamp'].apply(lambda date: date.split(' ')[0])
        user_view_df['time'] = user_view_df['time_stamp'].apply(lambda date: date.split(' ')[1])
        user_view_df.set_index('shop_id', drop=True, inplace=True)
        user_pay_se = user_view_df['day']
        df_view = DataFrame()
        count = 0
        for shop_id in np.unique(user_view_df.index):
            shop_se = user_pay_se[shop_id]
            shop_count = shop_se.value_counts()
            shop_count = shop_count[shop_count.notnull()]
            shop_df = DataFrame(shop_count)
            shop_df['shop_id'] = shop_id
            df_view = df_view.append(shop_df)
            count += 1
            print(count)
            gc.collect()
        df_view.reset_index(inplace=True)
        df_view.rename(columns={'day': 'result', 'index': 'day'}, inplace=True)
        df_view = df_view.sort_values(by=['shop_id', 'day'])
        df_view.reset_index(inplace=True, drop=True)
        df_view.to_excel('view_new.xlsx', encoding='utf-8')

    def add_view_data(self):
        # 添加浏览特征
        df_view = pd.read_excel('view_new.xlsx', encoding='utf-8')
        df_view.rename(columns={'result': 'view_result'}, inplace=True)
        df_pay = pd.read_excel('pay_new_4.xlsx', encoding='utf-8')
        df_pay = pd.merge(df_pay, df_view, how='left')
        df_pay.to_excel('pay_new_5.xlsx', encoding='utf-8')

    def build_ma_data(self):
        df_ma = DataFrame()

        def ma(shop_data):
            global df_ma
            date_list = list(shop_data.index)
            for i in range(14):
                day = '%02d' % (i + 1)
                date_list.append('2016-11-' + day)
            shop_id = shop_data.name
            threshold = shop_data.mean() * 0.15
            shop_data = shop_data.apply(lambda x: 'NaN' if x < threshold else x)
            shop_data = shop_data.fillna('NaN')
            shop_result_list = list(shop_data)
            shop_ma_list = [None] * 14
            for i in range(14, len(shop_result_list) + 14):
                if i - 21 < 0:
                    index_left = 0
                else:
                    index_left = i - 21
                interval = shop_result_list[index_left: i - 14]
                interval = [n for n in interval if n and not isinstance(n, str)]
                if interval:
                    result = sum(interval) / len(interval)
                else:
                    neibor_list = shop_result_list[0:i]
                    neibor_list = [v for v in neibor_list if v and not isinstance(v, str)]
                    neibor_list = neibor_list[-3:]
                    if neibor_list:
                        result = sum(neibor_list) / len(neibor_list)
                    else:
                        result = None
                shop_ma_list.append(result)
            df = DataFrame(shop_ma_list)
            df.index = date_list
            df['shop_id'] = shop_id
            df_ma = df_ma.append(df)

        DF = pd.read_excel(r'pay_old.xlsx', encoding='utf-8')
        DF.apply(ma, axis=1)
        df_ma.reset_index(inplace=True)
        df_ma.rename(columns={0: 'ma_7', 'index': 'day'}, inplace=True)
        df_ma.to_excel('ma_7.xlsx', encoding='utf-8')

