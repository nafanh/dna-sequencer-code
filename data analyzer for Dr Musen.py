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

#Reads text file data and creates a dataframe
def table(file_name):
    df = pd.read_csv(file_name, delimiter='\t')
    min_area = int(input("Please enter the minimum area: "))
    df_areamin = df.loc[df['Area'].astype(int)> min_area]
    print(df_areamin)
    return df_areamin

#
def difference(table):
    num_list = table['Dye/Sample Peak'].tolist()
    peak_num = []
    for peak in num_list:
        peak_num.append(peak[-1])
    idx = 1
    table.insert(loc=idx,column='Num',value=peak_num)
    #table.set_index('Num',inplace=True)
    #print(table.columns.values.tolist())
    return table

#Function that finds the last two peaks
def last_two(b):
    c = []
    for i in range(1,len(b)-1):
        if b[i][-1] > b[i+1][-1] or b[i][-1] == b[i+1][-1]:
            c.append(b[i-1][0])
            c.append(b[i][0])
    c.append(b[len(b)-2][0])
    c.append(b[-1][0])
    return(c)
#Takes the last two peaks as the template and product
def parse_peak_num(df):
    a = df['Num'].values.astype(int).tolist()
    idx = df.index.values.astype(int).tolist()
    #print(idx)
    coor = list(zip(idx,a))
    print(coor)
   # b = [int(x) for x in a]
    c = last_two(coor)
    print(c)
    range_list = []
    df['First'] = np.nan
    df['Second'] = np.nan

    area_list = [df.loc[idx,'Area'] for idx in c]
    print(area_list)
    #List c has all the indexes
    for i in range(0,len(c)-1,2):
        df.at[c[i],'First'] = area_list[i]
        df.at[c[i+1],'Second'] = area_list[i+1]
        #print(df.loc[idx,'Area'])
    #print(df)
##    i = 0
##    while i < len(c):
##        for num in b:
##            if num
##    for i in range(len(a)):
##        if a[i] == '1':
##            range_list.append(i)
##    
##    for i in range(len(range_list)):
##        if i == len(range_list)-1:
##            first = len(a)-2
##            second = len(a)-1
##            df.loc[df.index[first],'First'] = df.iloc[first,5]
##            df.loc[df.index[second],'Second'] = df.iloc[second,5]
##            break
##        temp = []
##        after = range_list[i+1]
##        for j in range(after-2,after):
##            temp.append(j)
##        df.loc[df.index[temp[0]],'First'] = df.iloc[temp[0],5]
##        df.loc[df.index[temp[1]],'Second'] = df.iloc[temp[1],5]
##        #print(temp)
##    
        
        
    return df

#Adds the peaks if they aren't NaN values      
def add_frac(df):
    first_list = df['First'].values.tolist()
    second_list = df['Second'].values.tolist()
    fix_first_list = [x for x in first_list if str(x) != 'nan']
    fix_second_list = [x for x in second_list if str(x) != 'nan']
    add = [x + y for x,y in zip(fix_first_list,fix_second_list)]
    return add

#Function takes in add_frac list and returns the fractional area
def frac(prod_list,df):
    first_list = df['First'].values.tolist()
    fixed = [x for x in first_list if str(x) != 'nan']
    frac_list = [x / y for x,y in zip(fixed,prod_list)]
    return frac_list

#Fixes fractional area for concentration
def frac_conc_fix(frac):
    conc = int(input("Please enter concentration(nM): "))
    a = [x * conc for x in frac]
    #a[0] = 0
    return a

#Prompts the user for time points and adds to dataframe
#Also adds the product to another column
def time_addition(frac_conc):
    cont = 'y'
    #time_pts = [x for x in range(16)]
    time_pts = []
    while cont == 'y' or cont == 'Y':
        time = input("Please enter a time values: ")
        time_pts = time.split(',')
        cont = input("Are there any more time points? Enter 'y' for yes or 'n' for no: ")
    df = pd.DataFrame(time_pts,columns = ['Time'])
    print(len(df))
    df['Product'] = frac_conc
    export_data = df.to_csv('Exported_data.csv',sep=',')
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

if __name__ == '__main__':
    main()
