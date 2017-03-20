# coding:utf-8
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import numpy as np
import xgboost as xgb


class MachineLearning:
    def __init__(self):
        df_feature_data = pd.read_excel('feature_data.xlsx', encoding='utf-8')
        print(df_feature_data.columns)
        self.train_xData = df_feature_data.ix[:599274]
        self.train_yData = self.train_xData['result']
        self.train_xData.drop('result', axis=1, inplace=True)
        self.test_xData = df_feature_data.ix[599275:]
        self.test_xData.drop('result', axis=1, inplace=True)

    def normalize(self):
        scaler = preprocessing.StandardScaler().fit(self.train_xData.values)
        self.train_xData = DataFrame(scaler.transform(self.train_xData), index=self.train_xData.index, columns=self.train_xData.columns)
        self.test_xData = DataFrame(scaler.transform(self.test_xData), index=self.test_xData.index, columns=self.test_xData.columns)
        normalizer = preprocessing.Normalizer().fit(self.train_xData.values)
        self.train_xData = DataFrame(normalizer.transform(self.train_xData), index=self.train_xData.index, columns=self.test_xData.columns)
        self.test_xData = DataFrame(normalizer.transform(self.test_xData), index=self.test_xData.index, columns=self.test_xData.columns)

    def GBDT(self):
        self.normalize()
        GBDT = GradientBoostingRegressor(n_estimators=2000, max_depth=7, min_samples_leaf=60, min_samples_split=1200, subsample=0.7)
        GBDT.fit(self.train_xData, self.train_yData)
        result = GBDT.predict(self.test_xData)
        GBDT_result = np.array(result).reshape(2000, 14)
        GBDT_predict = DataFrame(GBDT_result)
        GBDT_predict.to_excel('GBDT.xlsx', encoding='utf-8')
        print(GBDT.score(self.train_xData,self.train_yData))

    def xgbst(self):
        for f in self.train_xData.columns:
            if self.train_xData[f].dtype == 'object':
                lbl = preprocessing.LabelEncoder()
                lbl.fit(list(self.train_xData[f].values))
                self.train_xData[f] = lbl.transform(list(self.train_xData[f].values))

        for f in self.test_xData.columns:
            if self.test_xData[f].dtype == 'object':
                lbl = preprocessing.LabelEncoder()
                lbl.fit(list(self.test_xData[f].values))
                self.test_xData[f] = lbl.transform(list(self.test_xData[f].values))

        if self.train_yData.dtype == 'object':
            lbl = preprocessing.LabelEncoder()
            lbl.fit(list(self.train_yData.values))
            self.train_yData = lbl.transform(list(self.train_yData.values))

        self.train_xData.fillna(-999, inplace=True)
        self.test_xData.fillna(-999, inplace=True)

        self.train_xData = np.array(self.train_xData)
        self.train_xData.astype(float)
        self.test_xData = np.array(self.train_xData)
        self.test_xData.astype(float)

        train_xData = xgb.DMatrix(self.train_xData)
        train_yData = xgb.DMatrix(self.train_yData)
        test_xData = xgb.DMatrix(self.test_xData)
        params = {
            'objective': 'reg:logistic',
            'booster': 'gbtree',
            'scala_pos_weight': 1,
            'eval_metric': 'auc',
            'gamma': 0.1,
            'max_depth': 8,
            'lambda': 550,
            'subsample': 0.7,
            'colsample_bytree': 0.4,
            'min_child_weight': 3,
            'eta': 0.02,
            'nthread': 7
        }
        watchlist = [(train_yData, 'val'), (train_xData, 'train')]
        xgboost_model = xgb.train(params, train_xData, num_boost_round=3000, evals=watchlist)
        xgboost_predict_y = xgboost_model.predict(test_xData, ntree_limit=xgboost_model.best_ntree_limit)
        print(xgboost_predict_y)


class IndexGBDT():
    def __init__(self):
        self.df_feature_data = pd.read_excel('feature_data.xlsx', encoding='utf-8')
        self.df_feature_data.drop(['shop_level', 'city_name', 'per_pay', 'score', 'comment_cnt', 'tag_3'], axis=1, inplace=True)
        self.predict_df = DataFrame()
        print(self.df_feature_data.columns)

    def main(self):
        for shop_id in range(1, 2001):
            shop_df = self.df_feature_data[self.df_feature_data['shop_id'] == shop_id]
            shop_df.drop('shop_id', axis=1, inplace=True)
            length = len(shop_df['day'])
            shop_df['day'] = range(length)

            train_xData = shop_df.ix[:599274]
            train_yData = train_xData['result']
            train_xData.drop('result', axis=1, inplace=True)

            var = train_yData.var()

            test_xData = shop_df.ix[599275:]
            test_xData.drop('result', axis=1, inplace=True)
            scaler = preprocessing.StandardScaler().fit(train_xData.values)
            train_xData = DataFrame(scaler.transform(train_xData), index=train_xData.index, columns=train_xData.columns)
            test_xData = DataFrame(scaler.transform(test_xData), index=test_xData.index, columns=test_xData.columns)
            normalizer = preprocessing.Normalizer().fit(train_xData.values)
            train_xData = DataFrame(normalizer.transform(train_xData), index=train_xData.index, columns=test_xData.columns)
            test_xData = DataFrame(normalizer.transform(test_xData), index=test_xData.index, columns=test_xData.columns)

            GBDT = GradientBoostingRegressor(n_estimators=1200, max_depth=7)
            GBDT.fit(train_xData, train_yData)
            print(shop_id, GBDT.score(train_xData, train_yData))
            result = GBDT.predict(test_xData)
            result_list = list(result)
            result_list.append(var)
            result_list.append(length)
            result_df = DataFrame(result_list).T
            self.predict_df = self.predict_df.append(result_df)

    def predict_process(self):
        self.main()
        self.predict_df.index = range(1, 2001)
        self.predict_df.to_excel(r'index_GBDT.xlsx', encoding='utf-8')


if __name__ == '__main__':
    ML = MachineLearning()
    ML.GBDT()
    # ML.xgbst()
    # index_gbdt = IndexGBDT()
    # index_gbdt.predict_process()
