import pandas as pd
import numpy as np
import re
import pprint


def filtered_data(name):
    # file_name = 'Burst on PThio DNA.txt'
    f = open(name, 'r')
    headers = ['Dye', 'Peak Number', 'Height', 'Time', 'Well', 'Area', 'Data Point']
    # data = pd.read_csv('Burst on PThio DNA.txt')
    f.readline()
    col_data = []
    count = 0
    for test in f:
        test_set = test.split()
        # strips the underscore in long description
        desc_fix = test_set[1].split('_')
        # print(desc_fix)
        # removes long description name
        test_set.pop(1)
        # print(test_set)
        # print(test_set)
        test_set.insert(2, desc_fix[2])
        test_set.insert(3, desc_fix[len(desc_fix) - 1])
        # print(test_set)
        # splits dye and peak number
        dye_peak = test_set[0].strip('\"').replace(',', '')
        test_set.pop(0)
        i = 0
        while i < len(dye_peak):
            test_set.insert(i, dye_peak[i])
            i += 1
        # print(test_set)
        col_data.append(test_set)
        count += 1
    # pprint.pprint(col_data)
    df = pd.DataFrame(col_data, columns=headers)

    # filters height above 100
    df_h100 = df.loc[df['Height'].astype(int) > 100]

    # exports data with height above 100 to excel sheet
    # export_excel_filtered = df.to_csv('Export_data_filtered.csv',sep=',')

    return df_h100


def sample_distance(filtered_data):
    # gets peaks without internal standard
    df_no_int = filtered_data.loc[filtered_data['Dye'] == 'B']

    # print(df_no_int)

    # gets peaks with internal standard
    df_int_std = filtered_data.loc[filtered_data['Dye'] == 'Y']
    # print(df_int_std)

    # makes list of int standard data points
    int_stdlist = df_int_std['Data Point'].tolist()

    # makes list of int standard time points
    int_stdtimelist = df_int_std['Time'].tolist()

    # makes list of sample data points
    sample_list = df_no_int['Data Point'].tolist()

    # makes list of sample time points
    sample_timelist = df_no_int['Time'].tolist()
    # print(sample_timelist)

    int_std_dict = dict(zip(int_stdtimelist, int_stdlist))
    sample_2d = [list(a) for a in zip(sample_timelist, sample_list)]

    # if sample_2d[i][0] in int_std_dict:
    diff_list = []
    for i in range(len(sample_2d)):
        diff = int(int_std_dict[sample_2d[i][0]]) - int(sample_2d[i][1])
        diff_list.append(diff)

    df_no_int['Diff'] = diff_list
    return (df_no_int)

    # exports data with compared to internal standard
    # export_excel_difference = df.to_csv('Export_data_difference.csv',sep=',')


# Outputs the polymer size (ex: 28mer)
def size(df):
    original = int(input('Please enter the template size: '))
    df["Size"] = df["Peak Number"].astype(int) + (original - 1)
    return df

def table(df):
    df_time = list(set(df['Time'].tolist()))
    df_time.sort()
    df_size = list(set(df['Size'].tolist()))
    df_size.sort()
    #n = pd.DataFrame(columns = df_size)
    # headings = df_size
    # headings.append('Total')
    # for i in range(len(df_size)-1):
    #     headings.append(str(df_size[i]) + '/' + headings[len(headings)-1-i])
    # n = pd.DataFrame(df_time,columns=['Time'])
    #  for i in range(len(headings)):
    #      n[headings[i]] = np.nan
    #n.set_index('Time',inplace=True)

    area_list = df['Area'].tolist()
    time_list = df['Time'].astype(float).tolist()
    # time_dict = {'time':time_list}
    size_list = df['Size'].tolist()
    two_keys = list(zip(time_list,size_list))
    new_dict = {}
    n = pd.DataFrame()
    n.index.name = 'Time'
    for i in range(len(two_keys)):
        new_dict[two_keys[i]] = area_list[i]

    for key in two_keys:
        time = key[0]
        size = str(key[1]) + 'mer'
        n.loc[time,size] = int(new_dict[key])

    n['Total'] = n.sum(axis=1)
    headers_list = n.columns.values.tolist()
    for i in range(len(headers_list)-1):
        divide_name = headers_list[i] + '/' + headers_list[-1]
        n[divide_name] = n.iloc[:,i] / n.iloc[:,len(headers_list)-1]



    return n

def conc_fix(df):
    conc = int(input("Please enter the concentration: "))
    headers = df.columns.values.tolist()
    for head in headers:
        if '/Total' in head:
            df.loc[:,head] = df.loc[:,head] * conc
    return df
def main():
    name = input('Enter file name (.txt): ')
    filtered = filtered_data(name)
    int_std_dist = sample_distance(filtered)
    polymer = size(int_std_dist)
    print('Here is the Data:')
    print('--------------------------------------------------------')
    print(polymer)
    a = table(polymer)
    print(a)
    # print(int_std_dist)
    fix = conc_fix(a)
    print(fix)


main()
