import pandas as pd
data=pd.read_csv('merged_data_1.csv')
data['top_bottom']=str(data['Tops'])+str(data['Bottom'])

for i in range(data.shape[0]):
    data.loc[i,'top_bottom']=str(data.loc[i,'Tops'])+str(data.)