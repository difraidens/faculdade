# Importações
import pandas as pd
import numpy as np
import time
from datetime import datetime, date

#import matplotlib.pyplot as plt
#from asyncio.windows_events import NULL
import statistics
import serial
#Funcao para pegar as datas correntes do dia atual
def add_years(start_date, years):
    try:
        return start_date.replace(year=start_date.year - years)
    except ValueError:
        return start_date.replace(year=start_date.year - years, day=28)

# Atribuição de Datas
today = datetime.now()
today_last_year = add_years(today, 1)
today_string = today.strftime('%d/%m/%Y')
print("Hoje é:" + today_string + "\n\n")

# Ler o CSV
arquivo_csv1 = r'C:\Users\Matheus\Desktop\TCC\TCCBASEDADOS2.csv'
df_1 = pd.read_csv(arquivo_csv1,sep=';')

arquivo_csv2 = r'C:\Users\Matheus\Desktop\TCC\TCCVALIDACAO.csv'
df_2 = pd.read_csv(arquivo_csv2,sep=';')

arquivo_csv3 = r'C:\Users\Matheus\Desktop\TCC\TCCBASEDADOS.csv'
df_3 = pd.read_csv(arquivo_csv3,sep=';')

# Cria variáveis de contador e bases
baseTreinoInd = df_1['Data'].size
baseValidacaoInd = df_2['Data'].size
baseCompletaInd = df_3['Data'].size

# Cria os arrays com todos os dados
acompleta = [[0 for _ in range(5)]for _ in range(baseCompletaInd)]
avalidacao = [[0 for _ in range(5)]for _ in range(baseValidacaoInd)]
atreinamento = [[0 for _ in range(5)]for _ in range(baseTreinoInd)]

# Array para treinamento com 70% dos dados
contadorTrein = -1
for i in range(baseTreinoInd):
    
  contadorTrein += 1
  atreinamento[contadorTrein][0] = df_1.iloc[i,0]
  atreinamento[contadorTrein][1] = df_1.iloc[i,1]
  atreinamento[contadorTrein][2] = df_1.iloc[i,2]
  atreinamento[contadorTrein][3] = df_1.iloc[i,3]
  atreinamento[contadorTrein][4] = df_1.iloc[i,4]

atreinamento = np.asarray(atreinamento)         

# Inicializacao dos pesos Implementacao rede neural python
w = [0.1, 2, 0.4, 1]

# Treinamento Metodo gradiente pesos
X_1 = 1
X_2 = 2
X_3 = 3
Y = 4
learning_rate = 0.1

def z(S):
  return w[0] + w[1] * int(atreinamento[S][X_1]) + w[2] * int(atreinamento[S][X_2]) + w[3] * int(atreinamento[S][X_3])

def phi(z):
  if z > 0:
    return 1
  else:
    return 0

def J():
  return 1/2 * ((int(atreinamento[1][-1]) - phi(z(1)))**2 + (int(atreinamento[2][-1]) - phi(z(2)))**2 + (int(atreinamento[3][-1]) - phi(z(3)))**2 + (int(atreinamento[4][-1]) - phi(z(4)))**2)

#print("---1º Época---")
#print("Erro J(w) =", J())

def delta_j(j):
    
  if j == 1:
    for r in range(baseTreinoInd):
      varx = learning_rate * ((int(atreinamento[r][-1]) - phi(z(r))) * 1)
    return varx
  elif j == 2:
    for r in range(baseTreinoInd):
      varx = learning_rate*((int(atreinamento[r][-1]) - phi(z(r))) * int(atreinamento[r][X_1])) 
    return varx
  elif j == 3:
    for r in range(baseTreinoInd):
      varx = learning_rate*((int(atreinamento[r][-1]) - phi(z(r))) * int(atreinamento[r][X_2]))
    return varx
  elif j == 4:
    for r in range(baseTreinoInd):
      varx = learning_rate*((int(atreinamento[r][-1]) - phi(z(r))) * int(atreinamento[r][X_3])) 
    return varx

print("w inicial =", w)

epochs = 20000
for i in range(epochs):
  #print("---",i+2,"º Época---")
  #print("Erro J(w) =", J())
#Faz o ajuste dos pesos
  aux_0 = w[0] + delta_j(1)
  aux_1 = w[1] + delta_j(2)
  aux_2 = w[2] + delta_j(3)
  aux_3 = w[3] + delta_j(4)

  w = [aux_0, aux_1, aux_2, aux_3]

  #print("w =", w)
  #print("\n")
#Array para validacao com os dados
contadorTrein2 = -1
acert_count = 0
error_count = 0
for i in range(baseValidacaoInd):

  contadorTrein2 += 1
  avalidacao[contadorTrein2][0] = df_2.iloc[i,0]
  avalidacao[contadorTrein2][1] = df_2.iloc[i,1]
  avalidacao[contadorTrein2][2] = df_2.iloc[i,2]
  avalidacao[contadorTrein2][3] = df_2.iloc[i,3]
  avalidacao[contadorTrein2][4] = df_2.iloc[i,4]
  e1 = avalidacao[contadorTrein2][1]
  e2 = avalidacao[contadorTrein2][2]
  e3 = avalidacao[contadorTrein2][3]
  resposta = w[1]*e1+w[2]*e2+w[3]*e3+w[0]
#Tratamento da resposta para gerar em binário [0,1]  
  if resposta > 0:
    resposta = 1
  else:
    resposta = 0
#If e else para contar os registros certos e errados comparando com a coluna 4(Insolação) x (Insolacao prevista)  
  if resposta == avalidacao[contadorTrein2][4]:
    acert_count += 1
  else:
    error_count += 1  

avalidacao = np.asarray(avalidacao) 
total_count = acert_count + error_count

print("TOTAL DE VALIDAÇÕES: " + str(total_count))
print("ACERTOS: " +str(acert_count))
print("ERROS: " + str(error_count))

percentage = (acert_count / total_count) * 100
print('Porcentagem é %.2f' % percentage + '%')

#Pegar os dados completos no df_3
contadorTrein2 = -1
for i in range(baseCompletaInd):
    
  contadorTrein2 += 1
  acompleta[contadorTrein2][0] = df_3.iloc[i,0]
  acompleta[contadorTrein2][1] = df_3.iloc[i,1]
  acompleta[contadorTrein2][2] = df_3.iloc[i,2]
  acompleta[contadorTrein2][3] = df_3.iloc[i,3]
  acompleta[contadorTrein2][4] = df_3.iloc[i,4]

acompleta = np.asarray(acompleta) 

# Pegar os dados do dia corrente, media das entradas(Temp max, Temp med, Umidade)
entrada1 = [0 for _ in range(29)] #lista
entrada2 = [0 for _ in range(29)]
entrada3 = [0 for _ in range(29)]
for i in range (29):

    today_last_year = add_years(today, i+1)
    today_last_year_string = today_last_year.strftime('%d/%m/%Y')
    nova_data = today_last_year_string

    g = df_3.index[(df_3['Data']==nova_data)].tolist()

    if g != []:
        indice = g[0]    
        entrada1[i] = df_3.iloc[indice,1]
        entrada2[i] = df_3.iloc[indice,2]
        entrada3[i] = df_3.iloc[indice,3]
        tempMax = statistics.mode(entrada1)
        tempMed = statistics.mode(entrada2)
        Umidade = statistics.mode(entrada3)
#print(entrada1)
print(tempMax)
#print(entrada2)
print(tempMed)
#print(entrada3)
print(Umidade)
#Pega os pesos gerados  
print("w =", w)
#Faz a conta cruzando os pesos x entradas somados ao valor do peso bias
#Dados para testes com as diversas entradas
#tempMax = float(input("Entrada1: "))
#tempMed = float(input("Entrada2: "))
#Umidade = float(input("Entrada3: "))

resultado = w[1]*tempMax+w[2]*tempMed+w[3]*Umidade+w[0]

#Todos os cenarios com as diversas entradas
'''resultado = w[1]*1+w[2]*1+w[3]*1+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*1+w[2]*1+w[3]*0+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*1+w[2]*0+w[3]*1+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*0+w[2]*1+w[3]*1+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*0+w[2]*0+w[3]*0+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*0+w[2]*0+w[3]*1+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*0+w[2]*1+w[3]*0+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)
resultado = w[1]*1+w[2]*0+w[3]*0+w[0]
print("Insolacao <= 0 é 0, > 0 é 1 = ", resultado)'''

if resultado > 0:
  resultado = 1
else:
  resultado = 0
print("A Insolacao é: ",resultado)
  
#Mandar o retorno para ligar ou não ligar o arduino

try:
  conectado = serial.Serial("COM4",9600)
  time.sleep(60)

  volts = str(conectado.readline())
  volts = volts
  mediaVolts = float(volts[2:6])
  print(mediaVolts)

  if mediaVolts < 3.50 and resultado == 0:
    conectado.write(b'0')
    time.sleep(30)
    conectado.write(b'1')
    print("Conectado com a porta ", conectado.portstr)
  else:
    conectado.write(b'1')

except serial.SerialException:
  print("Porta USB não conectada!")
  pass
