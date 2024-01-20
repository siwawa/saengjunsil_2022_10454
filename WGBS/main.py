import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl


#df_CHH = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CHH', engine = 'openpyxl')
#df_CG = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CG', engine = 'openpyxl')
df_CHG = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CHG', engine = 'openpyxl')

#df_test = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'test', engine = 'openpyxl')
df_test = df_CHG

segment_ColFH = []
segment_ColAR = []
segment_ColGS = []
segment_CviFH = []
segment_CviAR = []
segment_CviGS = []
segment_SNPs = ''
segment_SVs = ''
segment_start_locs = ''
temp = []
fin_data = [] #[Chr, Start, Col-0 FH, AR, GS, Cvi FH, AR, GS, SNP, SV]

list = [segment_ColFH, segment_ColAR, segment_ColGS, segment_CviFH, segment_CviAR,
        segment_CviGS, temp]

def append():

    segment_ColFH.append(df_test['Col-0 FH'].tolist()[loc])
    segment_ColAR.append(df_test['Col-0 AR'].tolist()[loc])
    segment_ColGS.append(df_test['Col-0 GS'].tolist()[loc])
    segment_CviFH.append(df_test['Cvi FH'].tolist()[loc])
    segment_CviGS.append(df_test['Cvi AR'].tolist()[loc])
    segment_CviAR.append(df_test['Cvi GS'].tolist()[loc])

def append_to_fin():
    fin_data.append(
        {'Segnum': seg, 'Chr': chr, 'Location': [last*100000, (last+1)*100000], 'Col-0 FH': np.mean(segment_ColFH),
        'Col-0 AR': np.mean(segment_ColAR), 'Col-0 GS': np.mean(segment_ColGS), 'Cvi FH': np.mean(segment_CviFH),
        'Cvi AR': np.mean(segment_CviAR), 'Cvi GS': np.mean(segment_CviGS), 'SNP': segment_SNPs, 'SV': segment_SVs, 'Misc': segment_start_locs})

def append_blank():
    fin_data.append({'Segnum': seg, 'Chr': chr, 'Location': [last*100000, (last+1)*100000], 'Col-0 FH': "",
        'Col-0 AR': "", 'Col-0 GS': "", 'Cvi FH': "",'Cvi AR': "", 'Cvi GS': "", 'SNP': "", 'SV': "", 'Misc': 'blank'})


def cleanse():
    for segment in list:
        segment.clear()


chr = 1
seg = 0 #segment의 개수
last = 0 #마지막으로 10만개가 발견되었을 때의 first_loc
n_goback = 0 #얼마나 뒤로 가야 하는지
loc = 1
stop = False
print(df_test['Start'].tolist()[0])

while loc < len(df_test['Chr'].tolist()) :

    loc_now = df_test['Start'].tolist()[loc]
    loc_next = df_test['Start'].tolist()[loc+1]
    print(loc_now ,loc_next, last, chr, seg)
    flag = True

    while (((last) * 100000 < loc_now) and (loc_now < (last+1) * 100000)):
        loc_now = df_test['Start'].tolist()[loc]
        try:
            loc_next = df_test['Start'].tolist()[loc + 1]
        except IndexError:
            stop = True
            print("와!", seg, chr, "\n", segment_start_locs)
            append()
            segment_start_locs += (", " + str(loc_now))
            if df_test['SNP'].tolist()[loc] != "nan":
                segment_SNPs += (", " + str(df_test['SNP'].tolist()[loc]))
            if df_test['SV'].tolist()[loc] != "Unclassified":
                segment_SVs += (", " + str(df_test['SV'].tolist()[loc]))
            append_to_fin()
            # 여기다가 이제 dataframe data append
            print("끝끝끝~ ")
            break
        print(loc)

        segment_start_locs += (", " + str(loc_now))
        if df_test['SNP'].tolist()[loc] != "nan":
            segment_SNPs += (", " + str(df_test['SNP'].tolist()[loc]))
        if df_test['SV'].tolist()[loc] != "Unclassified":
            segment_SVs += (", " + str(df_test['SV'].tolist()[loc]))
        append()
        print("있어요", last,"00000 ~ ",last+1,"00000" , loc_now)
        loc += 1

        if chr != df_test['Chr'].tolist()[loc]:
            append_to_fin()
            seg += 1
            last = 0
            print("와!", seg, chr, "\n", segment_start_locs)
            # 여기다가 이제 dataframe data append
            chr = df_test['Chr'].tolist()[loc]
            cleanse()
            segment_SVs = ''
            segment_SNPs = ''
            segment_start_locs = ''
            if 'Mt' == df_test['Chr'].tolist()[loc] or 'Pt' == df_test['Chr'].tolist()[loc]:
                stop = True
            break

        if (loc_next > (last+1) * 100000) and (len(segment_start_locs) != 0):
            append_to_fin()
            seg += 1
            print("와!", seg, chr, "\n", segment_start_locs)
            #여기다가 이제 dataframe data append
            cleanse()
            segment_SVs = ''
            segment_SNPs = ''
            segment_start_locs = ''
            flag = False
            break

    if (loc_next > (last+1) * 100000) and (flag == True):
        print(loc_now, "없어요 >", (last+1) * 100000, flag)
        append_blank()
        last += 1

    if flag == False:
        last += 1

    if stop == True:
        break



print(fin_data)

df_heat = pd.DataFrame(fin_data, columns = ['Segnum', 'Chr', 'Location', 'Col-0 FH', 'Col-0 AR',
                                            'Col-0 GS', 'Cvi FH', 'Cvi AR', 'Cvi GS', 'SNP', 'SV' , 'Misc' ])
#df_heat.to_excel("pleasebee_fin_real.xlsx")
import matplotlib.pyplot as plt
import numpy as np

df_heat = df_heat.apply(pd.to_numeric, errors='coerce')
# create a numpy array of the data
data = df_heat[['Col-0 FH', 'Col-0 AR', 'Col-0 GS', 'Cvi FH','Cvi AR','Cvi GS']].values

# replace NaN values with 1
data[np.isnan(data)] = -1

fig, ax = plt.subplots()

# create a heatmap using pcolor function
heatmap = ax.pcolor(data.T, cmap='viridis', vmin =-1)

# add colorbar
cbar = plt.colorbar(heatmap)

# set tick labels
ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
# set tick labels for x and y axes
ax.set_yticklabels(df_heat.columns[3:], minor=False)

# define a function to get the x-coordinate of each chromosome boundary
def get_chr_boundaries(df):
    boundaries = []
    for chr_num in range(1, 6):
        loc_range = df.loc[df['Chr'] == float(chr_num), 'Location']
        print(loc_range)
        if not loc_range.empty:
            boundary = (loc_range.iloc[0], loc_range.iloc[-1])
            boundaries.append(boundary)
            print("yay", boundary)
    return boundaries

# get chromosome boundaries
chr_boundaries = get_chr_boundaries(df_heat)
print(chr_boundaries)

# add vertical lines at chromosome boundaries
for boundary in chr_boundaries:
    ax.axvline(boundary[0], color='white', lw=2)
    ax.axvline(boundary[1], color='white', lw=2)

def Number(i):
    i_location = 0
    for j in range(1,i+1):
        num_j = (df_heat['Chr'].tolist()).count(j)
        i_location += num_j

    num_i = (df_heat['Chr'].tolist()).count(i)
    print(i_location)
    i_location -= num_i/2
    return i_location

#num_mt = (df_heat['Chr'].tolist()).count('Mt')
#num_pt = (df_heat['Chr'].tolist()).count('Pt')
num_5 = (df_heat['Chr'].tolist()).count(5)

#print(Number(1),Number(2),Number(3),Number(4),Number(5), Number(5)+(num_5/2)+(num_mt/2), Number(5)+(num_5/2)+num_mt+(num_pt/2))
#plt.xticks(np.arange(0.5, len(df_heat.index), 1), df_heat['Chr']) - df_test 확인용, 돌리지 마세요!
ax.set_xticks([Number(1),Number(2),Number(3),Number(4),Number(5)])
ax.set_xticklabels(['1','2','3','4','5'])
# flip y-axis to show top-down view
ax.set_xlim([0, data.shape[0]])
ax.invert_yaxis()

# add title and axis labels
plt.title('CHG methylation regions of Col-0 and Cvi for each stages', fontsize = 20)
plt.xlabel('Chromosome numbers')
plt.ylabel('Ecotype and Growth stages')

plt.show()

