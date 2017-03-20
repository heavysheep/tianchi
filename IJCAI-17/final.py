# coding:utf-8
import pandas as pd
from pandas import DataFrame
# DF = pd.read_excel('GBDT.xlsx',encoding='utf-8')
# DF.index = range(1, 2001)
# DF = DF.apply(lambda x: x.apply(lambda y: int(y + 0.5)))
# print(DF)
# DF.to_csv(r'prediction_GBDT.csv', encoding='utf-8', header=False)

DF_1 = pd.read_excel(r'GBDT.xlsx', encoding='utf-8')
DF_1.index = range(1, 2001)
DF_2 = pd.read_excel(r'index_GBDT.xlsx', encoding='utf-8')
DF_2.index = range(1, 2001)

length_se = DF_2[15]
length_min = length_se.min()
length_max = length_se.max()
DF_2 = DF_2.loc[:, 0:13]

DF = DataFrame()
for i in range(1, 2001):
    balance = (length_se[i] - length_min) / (length_max - length_min) * 0.3 + 0.5
    df = DataFrame(DF_2.loc[i] * balance + DF_1.loc[i] * (1 - balance))
    DF = DF.append(df.T)

DF = DF.apply(lambda x: x.apply(lambda y: int(y + 0.5)))
DF.to_csv(r'prediction_DF_weight.csv', encoding='utf-8', header=False)