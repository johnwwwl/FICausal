import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source
import spicy

df=pd.read_csv('modified_merged_data.csv')
df.shape
df=df[['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
           'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
       'Top_Color_Sleeve',  'age', 'a', 'e', 'o', 'c', 'n']]
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['age', 'a', 'e', 'o', 'c', 'n']] = scaler.fit_transform(df[['age', 'a', 'e', 'o', 'c', 'n']])
categorical_columns=['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
          'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
             'Top_Color_Sleeve']
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# df_new=df[['Age', 'Gender', 'Race', 'Education_level',
#        'Income', 'Employment', 'Jobindustry', 'Working_hours',
#        'Working_pattern', 'Self_Regulation_MAD_Normalized', 'BMI',
#        'short_term_self_regulation','sleepduration_minutes', 'Feeling',
#        'Arousal', 'Fatigue', 'Wellbeing', 'Stress', 'Sleepquality', 'Location',
#        'VigorousPA_minutes', 'ModeratePA_minutes', 'Walking_minutes',
#        'physical_minutes', 'Sitting_minutes', 'ConfidencePA', 'DifficultyPA',
#        'Social_settings', 'Settings_where']]
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
outcomes=['a','e','o','c','n']
causal_graph =causal_graphs[0]
print(causal_graph)
outcome=outcomes[0]
causal_table=pd.DataFrame(columns=['treatment','outcome','P_value'])
variables=['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
         'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
     'Top_Color_Sleeve']

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
for v in variables:
  if v!='':
      print('==========================================================================')
      print(v)
      model=dowhy.CausalModel(
                data=df,
                graph=causal_graph.replace("\n",""),
                treatment=v,
                outcome=outcome
            )

      identified_estimand = model.identify_effect(proceed_when_unidentifiable=False)
      print(identified_estimand)
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
          print(v,outcome,estimate.value,p_value)
          causal_table = causal_table._append(
              {'treatment': v, 'outcome':outcome, 'estimate': estimate.value, 'P_value': p_value},
              ignore_index=True)
      except Exception as e:
          print(e)
      # if estimate.value!=0:
      #     res_random=model.refute_estimate(identified_estimand, estimate, method_name="random_common_cause", show_progress_bar=False)
      #     # print(res_random)
      #     res_placebo=model.refute_estimate(identified_estimand, estimate,
      #     method_name="placebo_treatment_refuter", show_progress_bar=False, placebo_type="permute")
      #     # print(res_placebo)
      #     res_subset=model.refute_estimate(identified_estimand, estimate,
      #     method_name="data_subset_refuter", show_progress_bar=False, subset_fraction=0.9)
      #     # print(res_subset)
      # causal_table=causal_table._append({'treatment':v,'outcome':'Wellbeing','estimate':estimate.value,'random':res_random,'placebo':res_placebo,'subset':res_subset},ignore_index=True)

sorted_df = causal_table.sort_values(by='estimate', key=lambda x: x.abs(),ascending=False)
print(sorted_df[['treatment','outcome','estimate','P_value']])

df=pd.read_csv('modified_merged_data.csv')