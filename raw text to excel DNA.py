import pandas as pd
import numpy as np
import re
import pprint
import matplotlib.pyplot as plt
import math
#Gets a number from string and sorts it into a list
#Two functions used for sorting the length of the polymers into columns
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)',text)]

#Removes the SettingCopyerror
#pd.options.mode.chained_assignment = None 

#Entered name has to be in this format:
# Any_Any_[Time]_Any(even amt of underscores)_[Well](.fsa)
#ex: Exo_BurstMM_0.5_TLD_2018-12-18_A06.fsa
def filtered_data(name):
    # file_name = 'Burst on PThio DNA.txt'
    f = open(name, 'r')
    headers = ['Dye', 'Peak Number', 'Height', 'Time', 'Well', 'Area', 'Data Point']
    # data = pd.read_csv('Burst on PThio DNA.txt')
    f.readline()
    col_data = []
    count = 0
    # reads each line in the text file
    for test in f:
        #Splits column data based on header
        # Dye/Sample Peak,Sample File Name,Size, Height, Area,Data Point
        test_set = test.split()
        #print(test_set)
        # strips the underscore in long description
        desc_fix = test_set[1].split('_')
        #print(desc_fix)
        # removes long description name
        test_set.pop(1)
        #print(test_set)
        #print(test_set)
        
        #inserts time into test_set
        test_set.insert(2, desc_fix[2])

        #inserts Well number at the end of test_set
        test_set.insert(3, desc_fix[len(desc_fix) - 1])
        #print(test_set)
        
        # splits dye and peak number and puts them into separate columns
        dye_peak = test_set[0].strip('\"').replace(',', '')
        test_set.pop(0)
        i = 0
        while i < len(dye_peak):
            test_set.insert(i, dye_peak[i])
            i += 1
        # print(test_set)
        # adding all data to each column
        col_data.append(test_set)
        count += 1
    # pprint.pprint(col_data)
    df = pd.DataFrame(col_data, columns=headers)
    #print(col_data)

    # filters height above user input. Note that if filter height
    # is above internal standard height, then error will raise
    # have to add try/except block here for future use
  
    min_height = int(input("Please enter the minimum height: "))
    df_hmin = df.loc[df['Height'].astype(int) > min_height]

    # exports data with height above 100 to excel sheet
    #export_excel_filtered = df.to_csv('Export_data_filtered_Hmin.csv',sep=',')
    f.close()
    return df_hmin


def sample_distance(filtered_data):
    # gets peaks without internal standard
    df_no_int = filtered_data.loc[filtered_data['Dye'] == 'B']
    #print(df_no_int)

    # gets peaks with internal standard
    df_int_std = filtered_data.loc[filtered_data['Dye'] == 'Y']
   
    #Exports the internal standard data
    export_int_std = df_int_std.to_csv('Export_data_int_std.csv',sep = ',')
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

    #pprint.pprint(sample_2d)
    
    # if sample_2d[i][0] in int_std_dict:
    diff_list = []
    for i in range(len(sample_2d)):
        diff = int(int_std_dict[sample_2d[i][0]]) - int(sample_2d[i][1])
        diff_list.append(diff)

    df_diff = df_no_int.copy()
    df_diff['Diff'] = diff_list

    # exports data with compared to internal standard
    #export_excel_difference = df.to_csv('Export_data_intstd_Diff.csv',sep=',')
    
    return (df_diff)

# Returns pandas series with list of unique ranges (distance from int. std.)
def diff_list(df):
    diff_set = df['Diff'].tolist()
    diff_set = sorted(list(set(diff_set)))
    return pd.Series(diff_set)


# Function that outputs the polymer size (ex: 28mer)
# and places it into a new column
# ****Have to edit to where the template size is in relation to difference***
def size(df):
    #Asks user input for template size
    #original = int(input('Please enter the template size: '))
    #Adjusts the peak number in relation to template size
    length = []
    ranges_list = []
    print("Please enter the diff bounds for each polymer. Ex: 27mer/300-400")
    addit = 'y'
    while addit == 'y' or addit == 'Y':
        temp = []
        polymer = input("Enter polymer (ex:27mer): ")
        length.append(polymer)
        while True:
            try:
                low_r = int(input("Enter lower bound of diff: "))          
                upper_r = int(input("Enter upper bound of diff: "))
                temp.append(low_r)
                temp.append(upper_r)
                ranges_list.append(temp)
                break
            except ValueError:
                print("Lower or upper bounds not valid. Please try again.")
        addit = input("Are there any more? Input 'y' for yes and 'n' to end: ")
    
    #ranges_list2 = sorted(ranges_list, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    
        
    ranges_dict = {}
    for i in range(len(ranges_list)):
        ranges_dict[length[i]] = ranges_list[i]
    #print(ranges_dict)

    diff_list = df['Diff'].astype(int).tolist()
    ranges_keys = list(ranges_dict.keys())
    #print(ranges_keys)
    final_length_list = []
    #print(diff_list)
    for j in diff_list:
        for i in range(len(ranges_keys)):
            width = ranges_dict[ranges_keys[i]]
            #print(ranges_dict[ranges_keys[i]])
            low = width[0]
            high = width[-1]
            if j >= low and j <= high:
                final_length_list.append(ranges_keys[i])
               
    #print(final_length_list)
            
    df["Size"] = final_length_list

    return df


# Returns a set list for x labels (size)
##def get_x_values(df):
##    df1 = list(set(df['Size'].tolist()))
##    print(df1)
##    length_list = list(set(df["Size"].tolist()))
##    length_list = sorted(length_list, key=lambda x: int("".join([i for i in x if i.isdigit()])))
#return length_list


# Function that creates the table containing area values for each polymer
def table(df):
    #Creates sorted set with time values (unique values only)
    df_time = list(set(df['Time'].tolist()))
    df_time.sort()

    #Creates sorted set with size values (unique values only)
    df_size = list(set(df['Size'].tolist()))
    df_size.sort(key=natural_keys)
    #print(df_size)
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

    #Creates dictionary where time and size are keys. Value is area
    size_list = df['Size'].tolist()
    
    #Creates tuple of time,size pairs
    two_keys = list(zip(time_list,size_list))
    #print(two_keys)
    
    new_dict = {}

    #Creates new empty dataframe with time values as index
    n = pd.DataFrame()
    n.index.name = 'Time'

    for size in df_size:
        n[size] = ""
    #print(n)
    #Appends area to dictionary containing the time and size keys
    for i in range(len(two_keys)):
        new_dict[two_keys[i]] = area_list[i]

    #Parses the dictionary and creates a new column in the table
    #for area
    for key in two_keys:
        time = key[0]
        size = key[1] 
        n.loc[time,size] = int(new_dict[key])

    #print(new_dict)
    #Creates new columns containing the area of each polymer/total
    n['Total'] = n.sum(axis=1)
    headers_list = n.columns.values.tolist()
    for i in range(len(headers_list)-1):
        divide_name = headers_list[i] + '/' + headers_list[-1]
        n[divide_name] = n.iloc[:,i] / n.iloc[:,len(headers_list)-1]

    #Sorts table by time and fill 'NaN' values with '0'
    n.sort_index(inplace=True)
    n = n.fillna(0)

    #Exports non-concentration fixed data
    #export_before_conc = n.to_csv('Export_data_Before_concfix.csv',sep=',')
    return n

# Returns a set list for x labels (size)
def get_size_values(df):
    df1 = list(set(df['Size'].tolist()))
    return df1

# Gets the values 
def get_frac_values(df):
    col_length = df.shape[1]
    midpt = int((col_length)/2) + 1
    df1 = df.iloc[:,midpt:]
    df1_values = df1.values.tolist()
    return df1_values
#Gets the time values from the index
def get_time_values(df):
    df_time = df.index.tolist()
    return df_time

#Function that multiplies values by specific concentration
def conc_fix(df):
    conc = int(input("Please enter the concentration(nM): "))

    #Creates new columns containing polymer/total multiplied by concentration
    headers = df.columns.values.tolist()
    for head in headers:
        if '/Total' in head:
            df.loc[:,head] = df.loc[:,head] * conc
    df = df.fillna(0)
    df.sort_index(inplace=True)

    #Exports the data to excel sheet
    #export = df.to_csv('Export_data_After_concfix.csv',sep=',')
    return df

# Makes plots of the fractional area vs size
def plot(time,size,frac):
    half = math.ceil(len(frac)/2)
    if half % 2 == 1:
            
        f,axarr = plt.subplots(math.ceil(len(frac)/2),2,sharex=True,sharey=True)
        f.suptitle('Fractional Area vs. Size')
        count = 0
        for i in range(2):
            for j in range(math.ceil(len(frac)/2)):
                if count == len(time):
                    break
                axarr[j,i].bar(size,frac[count],width=0.1)
                axarr[j,i].set_title('Time: ' + str(time[count]),loc='right',fontsize=8)
            #print(count)
                
                count+=1
    
    # Fix if odd number of time points
    else:
        f,axarr = plt.subplots(len(frac)//2 ,2,sharex=True,sharey=True)
        f.suptitle('Fractional Area vs. Size')
        count_even = 0
        for i in range(2):
            for j in range(len(time)//2):
                axarr[j,i].bar(size,frac[count_even],width=0.1)
                axarr[j,i].set_title('Time: ' + str(time[count_even]),loc='right',fontsize=8)
                #print(count)
                count_even+=1

        
    f.text(0.04,0.5,'Fractional Area', va='center', rotation='vertical')
    plt.subplots_adjust(hspace=0.4)
    plt.xticks(np.arange(len(size)),size)
    plt.xlabel('Size')
    #plt.ylabel('Fractional Area',labelpad=20)
    plt.show()
    
    
def main():
    name = input('Enter file name (.txt): ')
    filtered = filtered_data(name) #Creates table filtered by height threshold

    #Adds column to table for distance to int. std.
    int_std_dist = sample_distance(filtered)

    #Returns a pandas series of difference ranges\
    print('Here are the difference ranges between peak and internal standard: ')
    print(diff_list(int_std_dist))
    print(int_std_dist)

    #Creates a dataframe that filters out the internal standards and any peaks below certain threshold height
    polymer = size(int_std_dist)
    print('Here is the Data (Filters out heights below threshold. Note no internal std):')
    print('--------------------------------------------------------')
    print(polymer)
    #get_size_values(polymer)
    print()

    #Creates a dataframe the has the fractional area of each polymer before conc. fix
    a = table(polymer)
    print('Here is the data (Before concentration fix):')
    print('--------------------------------------------------------')
    print(a)

    #Gets the time, length, and fractional area into lists
    time = get_time_values(a)
    length = get_size_values(polymer)
    frac = get_frac_values(a)
   
    ##print(get_frac_values(a))
    ##print(a.index.values.tolist())
    print()
    # print(int_std_dist)

    #Creates a dataframe that updates fracitonal area for concentration
    fix = conc_fix(a)
    print()
    print('Here is the updated table data (after concentration fix):')
    print('--------------------------------------------------------')
    print(fix)

    #Plots the size, fractional area, and length using matplotlib
    #Returns a bar graph with time as the label
    plot(time,length,frac)





