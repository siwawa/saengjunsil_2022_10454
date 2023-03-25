import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

df_CHH = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CHH', engine = 'openpyxl')
df_CG = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CG', engine = 'openpyxl')
df_CHG = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CHG', engine = 'openpyxl')

#df_test = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'test', engine = 'openpyxl')
df_heat = df_CHH[['Chr', 'Col-0 FH', 'Col-0 AR', 'Col-0 GS', 'Cvi FH','Cvi AR','Cvi GS']]

fig, ax = plt.subplots()
heatmap = ax.pcolor(df_heat[['Col-0 FH', 'Col-0 AR', 'Col-0 GS', 'Cvi FH','Cvi AR','Cvi GS']].values.T)

def Number(i):
    i_location = 0
    for j in range(1,i+1):
        num_j = (df_heat['Chr'].tolist()).count(j)
        i_location += num_j

    num_i = (df_heat['Chr'].tolist()).count(i)
    print(i_location)
    i_location -= num_i/2
    return i_location

num_mt = (df_heat['Chr'].tolist()).count('Mt')
num_pt = (df_heat['Chr'].tolist()).count('Pt')
num_5 = (df_heat['Chr'].tolist()).count(5)

#print(Number(1),Number(2),Number(3),Number(4),Number(5), Number(5)+(num_5/2)+(num_mt/2), Number(5)+(num_5/2)+num_mt+(num_pt/2))
#plt.xticks(np.arange(0.5, len(df_heat.index), 1), df_heat['Chr']) - df_test 확인용, 돌리지 마세요!
ax.set_xticks([Number(1),Number(2),Number(3),Number(4),Number(5), Number(5)+num_5/2+(num_mt/2), Number(5)+num_5/2+num_mt+(num_pt/2)])
ax.set_xticklabels(['1','2','3','4','5', 'mt', 'pt'])
ax.set_yticks(np.arange(0.5, len(df_heat.columns) - 0.5, 1))
ax.set_yticklabels(['Col-0 FH', 'Col-0 AR', 'Col-0 GS', 'Cvi FH','Cvi AR','Cvi GS'])
plt.title('CHH methylation regions of Col-0 and Cvi for each stages', fontsize=20)
plt.xlabel('Probe location', fontsize=14)
plt.ylabel('Ecotype and Growth stages', fontsize=14)
plt.colorbar(heatmap)
plt.show()