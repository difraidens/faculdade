from asyncio.windows_events import NULL
from datetime import datetime
from email import header
from lib2to3.pgen2.pgen import DFAState
from posixpath import sep
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import array as ary
from datetime import datetime, date

def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year - years)
    except ValueError:
        # if Feb 29th doesn't exist, set to 28th)
        return start_date.replace(year=start_date.year - years, day=28)

today = datetime.now()
print("Hoje: " + str(today))
today_last_year = add_years(today, 1)
print("Hoje no ano anterior: " + str(today_last_year))

today_string = today.strftime('%d/%m/%Y')
print("Hoje é:" + today_string)


arquivo_csv1 = 'D:\Faculdade\8°Semestre\TCC\DadosInmetro\SaoPauloTCC2.csv'

df_1 = pd.read_csv(arquivo_csv1,sep=';')
print(df_1)
entrada = [[0 for _ in range(5)] for _ in range(25)]

for i in range (25):

    today_last_year = add_years(today, i+1)
    today_last_year_string = today_last_year.strftime('%d/%m/%Y')
    nova_data = today_last_year_string
    #print(df_1.loc[df_1['Data']==nova_data])  

    #print(nova_data)
    x = df_1.index[(df_1['Data']==nova_data)].tolist()
    
    if x == []:
        print("Lista vazia!")
    else:
            
        entrada[i][0] = df_1.iloc[x,1].values[0]
        entrada[i][1] = df_1.iloc[x,2].values[0]
        entrada[i][2] = df_1.iloc[x,3].values[0]
        entrada[i][3] = df_1.iloc[x,4].values[0]
        entrada[i][4] = df_1.iloc[x,5].values[0]

print(entrada)

#Proximo passo, criar um outro array sem os dados zerados 
'''
print(data)
print(concatenado)
teste_x = [insolacao1,precipitacao1,temperatura1,umidade1]
teste_y = [1,1,1,0]

#previsoes = modelo.predict(teste_x)
#print(previsoes)
   
if hora >= 6 and hora <= 18:
    tensao = 0.7
    if tensao >= 0.5:
        print('Tensao em nivel aceitavel')
    else:
        verif_chuva = data = row['Data']
'''

    