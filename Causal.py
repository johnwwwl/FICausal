import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz
from scipy.stats import pointbiserialr, f_oneway
target='n'
df=pd.read_csv('modified_merged_data.csv')

age_corr_with_a = df['age'].corr(df[target])

print(age_corr_with_a)

non_binary_categorical_features = [col for col in df.columns if df[col].nunique() > 2 and col not in ['age','a','e','o','c','n']]
anova_results = {}
for feature in non_binary_categorical_features:
    groups = [df[df[feature] == level][target] for level in df[feature].unique()]
    f_value, p_value = f_oneway(*groups)
    anova_results[feature] = {'F-value': f_value, 'P-value': p_value}

anova_low_p={}
anova_high_p={}
for i in anova_results.keys():
    if anova_results[i]['P-value']<0.05:
        anova_low_p[i]=anova_results[i]
    else:
        anova_high_p[i]=anova_results[i]
print(anova_low_p)
print(anova_high_p)