import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source
import spicy
import re

df=pd.read_csv('modified_merged_data.csv')
df.shape
df=df[['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
           'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
       'Top_Color_Sleeve',  'age', 'a', 'e', 'o', 'c', 'n']]

categorical_columns=['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
          'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
             'Top_Color_Sleeve']

origin='Hair_Style'
treat='Hair_Style_'
df_onehot = pd.get_dummies(df, columns=[origin], prefix=treat, prefix_sep='')
pattern = '^'+treat+'\d*$'
outcome='n'
outcomes=['a','e','o','c','n']
index=outcomes.index(outcome)
causal_graphs=['''digraph{
Tops[label=Tops];
Bottom[label=Bottom];
Color[label=Color];
Hair_Style[label=Hair_Style];
Hair_Color[label=Hair_Color];
Sleeve[label=Sleeve];
Tops_Bottom[label=Tops_Bottom];
Tops_Color[label=Tops_Color];
Color_Sleeve[label=Color_Sleeve];
Tops_Sleeve[label=Tops_Sleeve];
Top_Color_Sleeve[label=Top_Color_Sleeve];
a[lable=agreeableness];

Tops->a;
Hair_Style->a;
Tops_Bottom->a;
Tops_Color->a;
Tops_Sleeve->a;
Tops->Tops_Bottom;
Bottom->Tops_Bottom;
Sleeve->Tops_Bottom;
Tops->Tops_Color;
Color->Tops_Color;
Sleeve->Tops_Color;
Tops_Bottom->Tops_Color;
Tops->Tops_Sleeve;
Sleeve->Tops_Sleeve;
Tops_Color->Tops_Sleeve;
Color_Sleeve->Tops_Sleeve;
Color->Color_Sleeve;
Tops_Bottom->Color_Sleeve;
Tops_Color->Color_Sleeve;
Tops->Color_Sleeve;

}''','''digraph{
Tops[label=Tops];
Bottom[label=Bottom];
Color[label=Color];
Hair_Style[label=Hair_Style];
Hair_Color[label=Hair_Color];
Sleeve[label=Sleeve];
Tops_Bottom[label=Tops_Bottom];
Tops_Color[label=Tops_Color];
Color_Sleeve[label=Color_Sleeve];
Tops_Sleeve[label=Tops_Sleeve];
Top_Color_Sleeve[label=Top_Color_Sleeve];
e[lable=Extraversion];
Tops->e;
Hair_Style->e;
Tops_Bottom->e;
Tops_Color->e;
Tops_Sleeve->e;
Tops->Tops_Bottom;

Bottom->Tops_Bottom;
Sleeve->Tops_Bottom;
Tops_Sleeve->Tops_Bottom;
Tops->Tops_Color;
Color->Tops_Color;
Tops->Tops_Sleeve;
Sleeve->Tops_Sleeve;
Tops_Color->Tops_Sleeve;
Color_Sleeve->Tops_Sleeve;
Tops_Color->Bottom;
Tops_Color_Sleeve->Bottom;
Tops->Sleeve;

}
''',
               '''digraph{
               Tops[label=Tops];
               Bottom[label=Bottom];
               Color[label=Color];
               Hair_Style[label=Hair_Style];
               Hair_Color[label=Hair_Color];
               Sleeve[label=Sleeve];
               Tops_Bottom[label=Tops_Bottom];
               Tops_Color[label=Tops_Color];
               Color_Sleeve[label=Color_Sleeve];
               Tops_Sleeve[label=Tops_Sleeve];
               Top_Color_Sleeve[label=Top_Color_Sleeve];
               o[lable=o];
               Tops->Sleeve;
Hair_Style->Tops_Color_Sleeve;
Hair_Color->Tops_Color_Sleeve;

Hair_Style->o;
Hair_Color->o;

}''',
               '''digraph{
                            Tops[label=Tops];
                            c[lable=c];

                            Tops->c;
                            }''',
               '''digraph{
                            Tops[label=Tops];
                            Bottom[label=Bottom];
                            Color[label=Color];
                            Hair_Style[label=Hair_Style];
                            Hair_Color[label=Hair_Color];
                            Sleeve[label=Sleeve];
                            Tops_Bottom[label=Tops_Bottom];
                            Tops_Color[label=Tops_Color];
                            Color_Sleeve[label=Color_Sleeve];
                            Tops_Sleeve[label=Tops_Sleeve];
                            Top_Color_Sleeve[label=Top_Color_Sleeve];
                            n[lable=n];
Tops->Tops_Sleeve;
Sleeve->Tops_Sleeve;
Tops->Tops_Color;
Color->Tops_Color;
Tops->Color_Sleeve;
Color->Color_Sleeve;
Sleeve->Color_Sleeve;
Tops->Tops_Bottom;
Bottom->Tops_Bottom;
Sleeve->Tops_Bottom;
Tops->Tops_Sleeve;
Sleeve->Tops_Sleeve;
Tops->Tops_Color;
Tops->Tops_Sleeve;
Color->Tops_Color;
Sleeve->Tops_Color;
Sleeve->Tops_Sleeve;
Sleeve->Tops_Color;

Tops_Color->Tops_Sleeve;
Color_Sleeve->Tops_Sleeve;
Tops_Sleeve->Tops_Bottom;
Tops_Color->Tops_Sleeve;
Color_Sleeve->Tops_Sleeve;

Tops->n;
Hair_Style->n;
Sleeve->n;
Tops_Sleeve->n;
                            }'''
                                             ]
causal_graph=causal_graphs[index]
tops_columns = [col for col in df_onehot.columns if re.match(pattern, col)]
print(tops_columns)
causal_table=pd.DataFrame(columns=['treatment','outcome','P_value'])
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
for v in tops_columns:
    df1=df
    df1[origin]=df_onehot[v]
    model = dowhy.CausalModel(
        data=df1,
        graph=causal_graph.replace("\n", ""),
        treatment=origin,
        outcome=outcome
    )
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=False)
    # print(identified_estimand)
    estimate = model.estimate_effect(identified_estimand,
                                     method_name="backdoor.linear_regression")
    try:
        estimate_value = estimate.value
        standard_error = estimate.get_standard_error()

        z_score = estimate_value / standard_error
        p_value = 2 * (1 - spicy.stats.norm.cdf(abs(z_score)))

        significance_level = 0.05
        if p_value < significance_level:
            if estimate_value > 0:
                direction = "positive"
            elif estimate_value < 0:
                direction = "negative"
            else:
                direction = "none"  # This would be unusual for a significant effect
        else:
            direction = "not significant"

        # print(f"The ATE is {direction} and {'significant' if estimate_value < significance_level else 'not significant'}.")
        print(v, outcome, estimate.value, p_value)
        causal_table = causal_table._append(
            {'treatment': v, 'outcome': outcome, 'estimate': estimate.value, 'P_value': p_value},
            ignore_index=True)
    except Exception as e:
        print(e)
sorted_df = causal_table.sort_values(by='estimate', key=lambda x: x.abs(),ascending=False)
print(sorted_df[['treatment','outcome','estimate','P_value']])
sorted_df.to_csv('teest.csv',index=False)