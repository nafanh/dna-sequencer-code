import pandas as pd
import pprint as p
import numpy as np

##def filter_name(file):
##    f = open(file,'r')
##    desc = f.readline()   
##    desc_list = desc.split()
##    for line in f:
##        desc_line = line.split()
##        p.pprint(desc_line)
##        
##    #return desc_list

#def headers(h_list):

def table(file_name):
    df = pd.read_csv(file_name, delimiter='\t')
    return df

def difference(table):
    num_list = table['Dye/Sample Peak'].tolist()
    peak_num = []
    for peak in num_list:
        peak_num.append(peak[-1])
    idx = 1
    table.insert(loc=idx,column='Num',value=peak_num)
    #table.set_index('Num',inplace=True)
    

    
    return table

def parse_peak_num(df):
    a = df['Num'].values.tolist()
    range_list = []
    df['First'] = np.nan
    df['Second'] = np.nan
    for i in range(len(a)):
        if a[i] == '1':
            range_list.append(i)
    
    for i in range(len(range_list)):
        if i == len(range_list)-1:
            first = len(a)-2
            second = len(a)-1
            df.loc[df.index[first],'First'] = df.iloc[first,5]
            df.loc[df.index[second],'Second'] = df.iloc[second,5]
            break
        temp = []
        after = range_list[i+1]
        for j in range(after-2,after):
            temp.append(j)
        df.loc[df.index[temp[0]],'First'] = df.iloc[temp[0],5]
        df.loc[df.index[temp[1]],'Second'] = df.iloc[temp[1],5]
        #print(temp)
        
        
    return df
            
def add_frac(df):
    first_list = df['First'].values.tolist()
    second_list = df['Second'].values.tolist()
    fix_first_list = [x for x in first_list if str(x) != 'nan']
    fix_second_list = [x for x in second_list if str(x) != 'nan']
    add = [x + y for x,y in zip(fix_first_list,fix_second_list)]
    return add

def frac(prod_list,df):
    first_list = df['First'].values.tolist()
    fixed = [x for x in first_list if str(x) != 'nan']
    frac_list = [x / y for x,y in zip(fixed,prod_list)]
    return frac_list

def frac_conc_fix(frac):
    conc = int(input("Please enter concentration(nM): "))
    a = [x * conc for x in frac]
    a[0] = 0
    
    return a

def time_addition(frac_conc):
    cont = 'y'
    #time_pts = [x for x in range(16)]
    time_pts = []
    while cont == 'y' or cont == 'Y':
        time = input("Please enter a time values: ")
        time_pts = time.split(',')
        cont = input("Are there any more time points? Enter 'y' for yes or 'n' for no: ")
    df = pd.DataFrame(time_pts,columns = ['Time'])
    df['Product'] = frac_conc
    #export_data = df.to_csv('Exported_data.csv',sep=',')
    return df
def main():
##    file_name = input("Enter file name (.txt format): ")
##    df = pd.read_csv(file_name,delimiter='\t')
##    f = open(file_name,'r')
##    headers = f.readline()
##    headers_list = headers.split()
    #df.columns = headers_list
    
    file = input("Please enter file name(.txt format): ")
    a = table(file)
    b = difference(a)
    c = parse_peak_num(b)
    d = add_frac(c)
    e = frac(d,c)
    f = frac_conc_fix(e)
    g = time_addition(f)
    #print(a)
    p.pprint(b)
    p.pprint(c)
    p.pprint(d)
    p.pprint(e)
    p.pprint(f)
    p.pprint(g)
main()
