# coding:utf-8
import pandas as pd
import numpy as np
import gc


class FeatureEngineering:
    def __init__(self):
        self.feature_df = pd.read_excel(r'pay_new_5.xlsx', encoding='utf-8')
        self.day_index_save = list(np.unique(self.feature_df['day']))
        self.day_index_save.sort()

    def feature_digital(self):
        city_name_uniquelist = list(np.unique(self.feature_df['city_name']))
        self.feature_df['city_name'] = self.feature_df['city_name'].apply(lambda x: city_name_uniquelist.index(x))
        tag_1_uniquelist = list(np.unique(self.feature_df['tag_1']))
        self.feature_df['tag_1'] = self.feature_df['tag_1'].apply(lambda x: tag_1_uniquelist.index(x))
        tag_2_uniquelist = list(np.unique(self.feature_df['tag_2']))
        self.feature_df['tag_2'] = self.feature_df['tag_2'].apply(lambda x: tag_2_uniquelist.index(x))
        tag_3_uniquelist = list(np.unique(self.feature_df['tag_3']))
        self.feature_df['tag_3'] = self.feature_df['tag_3'].apply(lambda x: tag_3_uniquelist.index(x))
        gc.collect()

    def add_ma7(self):
        df_ma7 = pd.read_excel(r'ma_7.xlsx', encoding='utf-8')
        self.feature_df = pd.merge(self.feature_df, df_ma7, how='left')

    def add_mean(self):
        df_mean = pd.read_excel(r'mean.xlsx', encoding='utf-8')
        self.feature_df = pd.merge(self.feature_df, df_mean, how='left')

    def weather_level_process(self):
        def weather_level(weather):
            if isinstance(weather, str):
                if '小' in weather:
                    return 1
                elif '雨' in weather or '雪' in weather:
                    return 2
                else:
                    return 0
        self.feature_df['weather'] = self.feature_df['weather'].apply(weather_level)
        gc.collect()

    def fill_data(self):
        self.feature_df['weather'].fillna(method='pad', inplace=True)
        self.feature_df.fillna(
            {
                'score': self.feature_df['score'].mean(),
                'comment_cnt': self.feature_df['comment_cnt'].mean()
                                }, inplace=True)
        gc.collect()

    def drop_miss_and_bad(self):
        self.feature_df.drop(['view_result', 'tag_1', 'tag_2'], axis=1, inplace=True)
        self.feature_df = self.feature_df[self.feature_df['result'].notnull()]
        self.feature_df = self.feature_df[self.feature_df['mean'].notnull()]
        # self.feature_df = self.feature_df[self.feature_df['ma_7'].notnull()]
        self.feature_df = self.feature_df[self.feature_df['high'].notnull()]
        gc.collect()

    def day_index_screening(self):
        self.day_index_save = self.day_index_save[self.day_index_save.index('2015-10-12'):]
        self.day_index_save = self.day_index_save[:self.day_index_save.index('2016-02-08')] + \
                              self.day_index_save[self.day_index_save.index('2016-02-15'):]
        self.feature_df = self.feature_df[self.feature_df['day'].isin(self.day_index_save)]
        self.feature_df['day'] = self.feature_df['day'].apply(lambda x: self.day_index_save.index(x))
        gc.collect()

    def main(self):
        self.feature_digital()
        # self.add_ma7()
        self.add_mean()
        self.weather_level_process()
        self.fill_data()
        self.drop_miss_and_bad()
        self.day_index_screening()
        self.feature_df.to_excel(r'feature_data.xlsx', encoding='utf-8')


if __name__ == '__main__':
    feature_engineering = FeatureEngineering()
    feature_engineering.main()
