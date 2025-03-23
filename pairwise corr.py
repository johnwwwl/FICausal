import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz
from scipy.stats import pointbiserialr, f_oneway
from scipy.stats import chi2_contingency
from scipy import stats
from scipy.stats import pearsonr

target='a'
df=pd.read_csv('modified_merged_data.csv')
# df=df[['Tops', 'Bottom', 'Color', 'Hair_Style',
#           'Hair_Color', 'Sleeve', 'age', 'Tops_Bottom', 'Tops_Color',
#               'Color_Sleeve', 'Tops_Sleeve', 'Top_Color_Sleeve',target]]

cate=['Tops', 'Bottom', 'Color', 'Hair_Style',
          'Hair_Color', 'Sleeve', 'Tops_Bottom', 'Tops_Color',
              'Color_Sleeve', 'Tops_Sleeve', 'Top_Color_Sleeve']
conti=['age','a','e','o','c','n']

for i in range(len(df.columns)-2):
    for j in range(i+1,len(df.columns)):
        v1=df.columns[i]
        v2=df.columns[j]

        if v1 in cate and v2 in cate:
            pass
            # contingency_table = pd.crosstab(df[v1], df[v2])
            # chi2, p, dof, expected = chi2_contingency(contingency_table)
            # # print(f"\nChi-square Statistic: {chi2}")
            # # print(f"P-value: {p}")
            # # print(f"Degrees of Freedom: {dof}")
            # # print(f"Expected Frequencies:\n{np.array(expected)}")
        elif v1 in cate and v2 in conti:
            pass
            # grouped = df.groupby(v1)[v2].apply(list)
            # print(grouped)
            # f_value, p_value = stats.f_oneway(*grouped)
            # # print(f"F-value: {f_value}")
            # # print(f"P-value: {p_value}")
        elif v1 in conti and v2 in conti:
            print(v1, v2)
            df[v1] = df[v1].fillna(df[v1].mean())
            df[v2] = df[v2].fillna(df[v2].mean())

            correlation, p_value = pearsonr(df[v1], df[v2])
            print(f'Pearson correlation coefficient: {correlation}')
            print(f'P-value: {p_value}')
