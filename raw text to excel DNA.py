import pandas as pd
import re
import pprint 
file_name = 'Burst on PThio DNA.txt'
f = open(file_name,'r')
headers = ['Dye','Peak Number','Height','Time','Well','Area','Data Point']
#data = pd.read_csv('Burst on PThio DNA.txt')
f.readline()
col_data = []
count = 0
for test in f:
    test_set = test.split()
    #strips the underscore in long description
    desc_fix = test_set[1].split('_')
    #print(desc_fix)
    #removes long description name
    test_set.pop(1)
    #print(test_set)
    #print(test_set)
    test_set.insert(2,desc_fix[2])
    test_set.insert(3,desc_fix[len(desc_fix)-1])
    #print(test_set)
    #splits dye and peak number
    dye_peak = test_set[0].strip('\"').replace(',','')
    test_set.pop(0)
    i = 0
    while i < len(dye_peak):
        test_set.insert(i,dye_peak[i])
        i+=1
    #print(test_set)
    col_data.append(test_set)
    count += 1
#pprint.pprint(col_data)
df = pd.DataFrame(col_data,columns = headers)

#filters height above 100
df_h100 = df.loc[df['Height'].astype(int) > 100]
#print(df_h100)

#exports data with height above 100 to excel sheet
#export_excel_filtered = df.to_csv('Export_data_filtered.csv',sep=',')

#gets peaks without internal standard
df_no_int = df_h100.loc[df_h100['Dye'] == 'B']

#print(df_no_int)

#gets peaks with internal standard
df_int_std = df_h100.loc[df_h100['Dye'] == 'Y']
#print(df_int_std)

#makes list of int standard data points
int_stdlist = df_int_std['Data Point'].tolist()

#makes list of int standard time points
int_stdtimelist = df_int_std['Time'].tolist()

#makes list of sample data points
sample_list = df_no_int['Data Point'].tolist()

#makes list of sample time points
sample_timelist = df_no_int['Time'].tolist()
#print(sample_timelist)


int_std_dict =  dict(zip(int_stdtimelist,int_stdlist))
sample_2d = [list(a) for a in zip(sample_timelist,sample_list)]

#if sample_2d[i][0] in int_std_dict:
diff_list = []
for i in range(len(sample_2d)):
    diff = int(int_std_dict[sample_2d[i][0]]) - int(sample_2d[i][1])
    diff_list.append(diff)

df_no_int['Diff'] = diff_list
print(df_no_int)
               
    
