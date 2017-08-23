import pandas as pd
import os

datas_path = 'nba_2014_datas'

if os.path.isfile(datas_path+'.csv'):
    os.remove(datas_path+'.csv')
    print('yes')
index = 0
for file in os.listdir(datas_path):
    data_filename = os.path.join(datas_path, file)
    dataset = pd.read_csv(data_filename, parse_dates=[0])
    if index==0 :
        dataset.to_csv(datas_path+'.csv',index=False,mode='a+')
    else:
        dataset.to_csv(datas_path+'.csv',index=False,mode='a+',header=False)

    index += 1
