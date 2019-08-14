#!/usr/bin/env python3
from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import re
import pprint
import matplotlib.pyplot as plt
import math
import os
from pathlib import Path


# Gets a number from string and sorts it into a list
# Two functions used for sorting the length of the polymers into columns
def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


# Removes the SettingCopyerror
# pd.options.mode.chained_assignment = None

# Entered name has to be in this format:
# Any_Any_[Time]_Any(even amt of underscores)_[Well](.fsa)
# ex: Exo_BurstMM_0.5_TLD_2018-12-18_A06.fsa
# Ex: PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa
time_underscore = int(
    input("Please enter after which underscore the time is. (If time is before 1st underscore, enter 0: "))


# well_underscore = int(input("Please enter after which underscore the well num is: "))
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
        # Splits column data based on header
        # Dye/Sample Peak,Sample File Name,Size, Height, Area,Data Point

        test_set = test.split()
        # Output: ['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '894', '11056', '2524']

        # print(test_set)
        # strips the underscore in long description
        desc_fix = test_set[1].split('_')
        # Output: ['PT', '100nM', '0', 'TLD', '4.2.19', '1', '2019-04-02', 'A05.fsa']

        # print(desc_fix)
        # removes long description name
        test_set.pop(1)
        # Output: ['"B,1"','894', '11056', '2524']
        # print(test_set)
        # print(test_set)

        # inserts time into test_set
        test_set.insert(2, desc_fix[time_underscore])

        # Output:['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '0', '894', '11056', '2524']

        # inserts Well number at 4th position of test_set
        test_set.insert(3, desc_fix[len(desc_fix) - 1])

        # Output: #['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '0', 'A05.fsa', '894', '11056', '2524']

        # print(test_set)

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
    # print(col_data)

    # filters height above user input. Note that if filter height
    # is above internal standard height, then error will raise
    # have to add try/except block here for future use
    df_int_all = df.loc[df['Dye'] == 'Y']
    print("These are all the internal std. peaks\n")
    print('---------------------------------------')
    print(df_int_all)
    min_height = int(input("Please enter the minimum height (make sure \
bigger than int std desired): "))
    df_hmin = df.loc[df['Height'].astype(int) > min_height]

    # exports data with height above 100 to excel sheet
    # export_excel_filtered = df.to_csv('Export_data_filtered_Hmin.csv',sep=',')
    f.close()
    return df_hmin


def sample_distance(filtered_data):
    # gets peaks without internal standard
    df_no_int = filtered_data.loc[filtered_data['Dye'] == 'B']
    # print(df_no_int)

    # gets peaks with internal standard
    df_int_std = filtered_data.loc[filtered_data['Dye'] == 'Y']

    # Exports the internal standard data
    # export_int_std = df_int_std.to_csv('Export_data_int_std.csv',sep = ',')
    print()
    print('Here are the internal std. peaks filtered: ')
    print('-------------------------------------------------------')
    print(df_int_std)

    # makes list of int standard data points
    int_stdlist = df_int_std['Data Point'].tolist()

    # makes list of int standard time points
    int_stdtimelist = df_int_std['Time'].tolist()

    # makes list of sample data points
    sample_list = df_no_int['Data Point'].tolist()

    # makes list of sample time points
    sample_timelist = df_no_int['Time'].tolist()
    # print(sample_timelist)

    # zips the internal standard time points and data points into a dictionary
    # Ex: {1:2,3:4}
    int_std_dict = dict(zip(int_stdtimelist, int_stdlist))

    # zips the sample time points and data points into a nested list
    # Ex: [[1,2],[3,4]]
    sample_2d = [list(a) for a in zip(sample_timelist, sample_list)]

    # pprint.pprint(sample_2d)

    # if sample_2d[i][0] in int_std_dict:

    # Creates a column in the pandas dataframe for difference
    # (internal standard - sample) by using datapoint
    # For each time
    diff_list = []
    for i in range(len(sample_2d)):
        # Subtracts the internal std value by the sample datapoint
        # Method is inefficient, could probably use nested list
        # for the internal standards as well
        # int_std_dict is a dictionary, so sample_2d[i][0] takes the time pt and finds the key value pair
        #diff_sub = int(int_std_dict[sample_2d[i][0]]) - int(sample_2d[i][1])
        diff = int(int_std_dict[sample_2d[i][0]]) / int(sample_2d[i][1]) * 100
        diff_list.append(diff)

    # This is to prevent pandas SettingwithCopyWarning
    df_diff = df_no_int.copy()
    df_diff['Diff'] = diff_list

    # exports data with compared to internal standard
    # export_excel_difference = df.to_csv('Export_data_intstd_Diff.csv',sep=',')

    # Returns a dataframe containing values with differences and
    # No intenal standard column
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
    # Asks user input for template size
    # original = int(input('Please enter the template size: '))
    # Adjusts the peak number in relation to template size

    # Polymer length list. Ex: [27mer,28mer,29mer]
    length = []

    # Nested list for the ranges of the difference ranges for each polymer.
    # Ex: For 27mer: [[300,400]]. Where 300 is lower bound and 400 is upper bound
    ranges_list = []

    # Prompts user for difference bounds for each polymer
    print("Please enter the diff bounds for each polymer. Ex: 27mer/300-400")
    addit = 'y'

    # Loop for multiple polymers
    while addit == 'y' or addit == 'Y':
        # Creates temporary list to be added to the ranges_list
        # Resets everytime the loop is run
        temp = []
        polymer = input("Enter polymer (ex:27mer): ")
        while True:
            if 'mer' not in polymer:
                polymer = input("Invalid polymer name, please try again: ")
            else:
                break
        length.append(polymer)
        while True:
            try:
                low_r = float(input("Enter lower bound of diff: "))
                upper_r = float(input("Enter upper bound of diff: "))
                temp.append(low_r)
                temp.append(upper_r)
                # Adds nested list of lower and upper bounds to list
                ranges_list.append(temp)
                break

            # In case integer not entered for bounds. Catch exception
            except ValueError:
                print("Lower or upper bounds not valid. Please try again.")
        addit = input("Are there any more? Input 'y' for yes and 'n' to end: ")

    # ranges_list2 = sorted(ranges_list, key=lambda x: int("".join([i for i in x if i.isdigit()])))

    # Creates a dictionary for polymer length and difference ranges
    # Ex: {27mer:[300,400],28mer"[450,500]}
    ranges_dict = {}

    # Loop appends each polymer as the key and the range list as the value
    for i in range(len(ranges_list)):
        ranges_dict[length[i]] = ranges_list[i]
    # print(ranges_dict)

    # Takes difference values to list
    diff_list = df['Diff'].astype(float).tolist()

    # Gets the keys of the dictionary which are the polymer sizes
    ranges_keys = list(ranges_dict.keys())
    # print(ranges_keys)
    final_length_list = []
    # print(diff_list)

    # Parses the differences (internal std - sample) and checks to see
    # If within a certain range. If it is, then it is appends the key(size)
    # to final_length_list
    for j in diff_list:
        for i in range(len(ranges_keys)):
            # Gets the value of ranges. Ex: [300,400]
            width = ranges_dict[ranges_keys[i]]
            # print(ranges_dict[ranges_keys[i]])

            # Takes lower bound
            low = width[0]
            # Takes upper bound
            high = width[-1]
            # If the difference is in between these bounds, then
            # append the size to the final_length_list
            if j >= low and j <= high:
                final_length_list.append(ranges_keys[i])

    # print(final_length_list)
    # Creates a new column in the dataframe for the size of each sample run
    df["Size"] = final_length_list

    return df


# Returns a set list for x labels (size)
##def get_x_values(df):
##    df1 = list(set(df['Size'].tolist()))
##    print(df1)
##    length_list = list(set(df["Size"].tolist()))
##    length_list = sorted(length_list, key=lambda x: int("".join([i for i in x if i.isdigit()])))
# return length_list


# Function that creates the table containing area values for each polymer
def table(df):
    # Creates sorted set with time values (unique values only)
    df_time = list(set(df['Time'].tolist()))
    df_time.sort()

    # Creates sorted set with size values (unique values only)
    df_size = list(set(df['Size'].tolist()))
    df_size.sort(key=natural_keys)

    # print(df_size)
    # n = pd.DataFrame(columns = df_size)
    # headings = df_size
    # headings.append('Total')
    # for i in range(len(df_size)-1):
    #     headings.append(str(df_size[i]) + '/' + headings[len(headings)-1-i])
    # n = pd.DataFrame(df_time,columns=['Time'])
    #  for i in range(len(headings)):
    #      n[headings[i]] = np.nan
    # n.set_index('Time',inplace=True)

    area_list = df['Area'].tolist()
    time_list = df['Time'].astype(float).tolist()
    # time_dict = {'time':time_list}

    # Creates dictionary where time and size are keys. Value is area
    size_list = df['Size'].tolist()

    # Creates tuple of time,size pairs
    # This tuple will eventually be the key values for the dictionary
    two_keys = list(zip(time_list, size_list))
    # print(two_keys)

    new_dict = {}

    # Creates new empty dataframe with time values as index
    n = pd.DataFrame()
    n.index.name = 'Time'

    for size in df_size:
        n[size] = ""
    # print(n)
    # Appends area to dictionary containing the time and size keys
    # Ex: {(0.05 sec,27mer),34000, (0.10 sec, 27mer), 20000}
    for i in range(len(two_keys)):
        new_dict[two_keys[i]] = area_list[i]

    # Parses the dictionary and creates a new column in the table
    # for area. Locates the time and size and inputs the area for that
    # those values into the dataframe
    for key in two_keys:
        time = key[0]
        size = key[1]
        n.loc[time, size] = int(new_dict[key])

    # print(new_dict)

    # Creates new columns containing the area of each polymer/total
    n['Total'] = n.sum(axis=1)
    headers_list = n.columns.values.tolist()
    for i in range(len(headers_list) - 1):
        divide_name = headers_list[i] + '/' + headers_list[-1]
        n[divide_name] = n.iloc[:, i] / n.iloc[:, len(headers_list) - 1]

    # Sorts table by time and fill 'NaN' values with '0'
    n.sort_index(inplace=True)
    n = n.fillna(0)

    # Exports non-concentration fixed data. Gives the fractional area for
    # Each polymer and the time points
    # export_before_conc = n.to_csv('Export_data_Before_concfix.csv',sep=',')
    return n


# Returns a set list for x labels (size)
def get_size_values(df):
    df1 = list(set(df['Size'].tolist()))
    df1.sort(key=natural_keys)
    return df1


# Gets the values
def get_frac_values(df):
    col_length = df.shape[1]
    midpt = int((col_length) / 2) + 1
    df1 = df.iloc[:, midpt:]
    df1_values = df1.values.tolist()

    return df1_values


# Gets the time values from the index
def get_time_values(df):
    df_time = df.index.tolist()
    return df_time


# Function that multiplies values by specific concentration
def conc_fix(df):
    conc = int(input("Please enter the concentration(nM): "))

    # Creates new columns containing polymer/total multiplied by concentration
    headers = df.columns.values.tolist()
    for head in headers:
        if '/Total' in head:
            df.loc[:, head] = df.loc[:, head] * conc
    df = df.fillna(0)
    df.sort_index(inplace=True)
    col_length = df.shape[1]
    midpt = int((col_length) / 2) + 1
    df_without = df.iloc[:, midpt:]
    csv_name = input("Please enter desired name of exported csv file: ")

    # Gets the time and concentration/total columns only
    col_length = df.shape[1]
    midpt = int((col_length) / 2) + 1
    df1 = df.iloc[:, midpt:]
    p = Path('Exported Data')
    p.mkdir(exist_ok=True)

    # Exports .txt file of polymer/total
    export_txt = df1.to_csv(os.getcwd() + '/' + str(p) + '/' + csv_name + '.txt', sep='\t')
    # Exports the data to excel sheet
    export = df.to_csv(os.getcwd() + '/' + str(p) + '/' + csv_name + '.csv', sep=',')
    # df_without_size = df.loc
    # Exports the data to excel sheet
    # export = df.to_csv('Export_data_After_concfix.csv',sep=',')
    return df


# ***Need to fixt this because matplotlib gives two columns. If you have
#   an odd number of time points, it will give you an empty graph****
# Makes bar graph plots of the fractional area vs size
# Function accepts time,size, and fraction list
def plot(time, size, frac):
    half = math.ceil(len(frac) / 2)
    # Conditional for odd number of time points
    if half % 2 == 1:
        # Creates a figure and adds subplots. Makes two columns
        f, axarr = plt.subplots(math.ceil(len(frac) / 2), 2, sharex=True, sharey=True)
        f.suptitle('Fractional Area vs. Size')
        count = 0
        # Adds subplot to each column
        for i in range(2):
            for j in range(math.ceil(len(frac) / 2)):
                if count == len(time):
                    break
                # Creates a bar graph subplot
                axarr[j, i].bar(size, frac[count], width=0.1)
                # Puts time in the upper right corner
                axarr[j, i].set_title('Time: ' + str(time[count]), loc='right', fontsize=8)
                axarr[j, i].set_yticks([0, 1])

                # print(count)

                count += 1

    # If even number of time points execute else statement
    else:
        f, axarr = plt.subplots(len(frac) // 2, 2, sharex=True, sharey=True)
        f.suptitle('Fractional Area vs. Size')
        count_even = 0
        for i in range(2):
            for j in range(len(time) // 2):
                axarr[j, i].bar(size, frac[count_even], width=0.1)
                axarr[j, i].set_title('Time: ' + str(time[count_even]), loc='right', fontsize=8)
                # print(count)
                count_even += 1

    # Labels the figure
    f.text(0.04, 0.5, 'Fractional Area', va='center', rotation='vertical')
    plt.subplots_adjust(hspace=0.4)
    # Labels the x-axis
    plt.xticks(np.arange(len(size)), size)
    plt.xlabel('Size')
    # plt.ylabel('Fractional Area',labelpad=20)
    plt.show()


def main():
    name = input('Enter file name (.txt): ')
    filtered = filtered_data(name)  # Creates table filtered by height threshold

    # Adds column to table for distance to int. std.
    int_std_dist = sample_distance(filtered)

    # Returns a pandas series of difference ranges
    print('Here are the difference ranges between peak and internal standard: ')
    print(diff_list(int_std_dist))
    print(int_std_dist)

    # Creates a dataframe that filters out the internal standards and any peaks below certain threshold height
    polymer = size(int_std_dist)
    print('Here is the Data (Filters out heights below threshold. Note no internal std):')
    print('--------------------------------------------------------')
    print(polymer)
    # get_size_values(polymer)
    print()

    # Creates a dataframe that has the fractional area of each polymer before conc. fix
    a = table(polymer)
    print('Here is the data (Before concentration fix):')
    print('--------------------------------------------------------')
    print(a)

    # Gets the time, length, and fractional area into lists
    time = get_time_values(a)
    length = get_size_values(polymer)
    frac = get_frac_values(a)

    ##print(get_frac_values(a))
    ##print(a.index.values.tolist())
    print()
    # print(int_std_dist)

    # Creates a dataframe that updates fracitonal area for concentration
    fix = conc_fix(a)
    print()
    print('Here is the updated table data (after concentration fix):')
    print('--------------------------------------------------------')
    print(fix)

    # Plots the size, fractional area, and length using matplotlib
    # Returns a bar graph with time as the label
    # plot(time,length,frac)


if __name__ == '__main__':
    main()

# Program works so you don't have to use the cmd line dir>/b

# In order to get the text file name from the folder
# Gets the x values
# a = [x for x in range(len(trace['DATA1'])+1)]
# for vectorization purposes
# array = np.arange(1,len(trace['DATA1'])+1)
# Parses each line of the text file

# Get the max value data
# max(trace['DATA1'])
# Gets the x value of the max value
# trace['DATA1'].index(max(trace['DATA1']))

# Prompts user for number of time points and the y/x min and max
# print(os.getcwd())
# Checks how many fsa files are in the directory. If not equal to the number
# of time points entered, then requests user to enter number of time points again
##folder_check = input("If your .fsa files are in a folder, press 'y' to continue, else press 'n': ")
##if folder_check == 'y' or folder_check == 'Y':
##    fsa_dir = input('Please enter the name of the folder with the .fsa files: ')
##    length_dir = len(os.listdir(fsa_dir + '/'))
##    length_dir_name = os.listdir(fsa_dir + '/')

# Make sure you have a folder that contains all the .fsa files
# Then make sure this script is outside of that folder

print()
print('-----------------------------------------------------------------------------')
print('Now aligning peaks....')
print('--------------------------------------------------------------')
print()
time_underscore = int(
    input("Please enter after which underscore the time is. (If time is before 1st underscore, enter 0: "))
folder_check = input("If your .fsa files are in a folder, press 'y' to continue, else press 'n': ")
if folder_check == 'y' or folder_check == 'Y':
    fsa_dir = input('Please enter the name of the folder with the .fsa files: ')
    dir_name = os.getcwd() + '\\' + fsa_dir
    os.chdir(dir_name)
    # print(os.getcwd())
# Checks number of .fsa files in the directory
fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
length_dir = len(fsa_names)
time_list = []
# Adjusts to make the zero time point the first .fsa file in the directory
for i in range(len(fsa_names)):
    name_list = fsa_names[i].split('_')
    time_value = name_list[time_underscore]
    if '.' not in time_value:
        time_list.append(int(time_value))
        continue
    time_list.append(float(time_value))
# Sorts time_list
time_list.sort()
print('Here are time time values detected in the folder with the .fsa files:')
print('--------------------------------------------------------------\n')
pprint.pprint(time_list)
fsa_names_sorted = []

for time in time_list:
    for ext_name in fsa_names:
        ext_name_split = ext_name.split('_')
        if ext_name_split[time_underscore] == str(time):
            fsa_names_sorted.append(ext_name)
        continue
print('The number of time points is:',len(time_list))
print('--------------------------------------------------------------')
print('Here are the file names the program is aligning:')
print('--------------------------------------------------------------\n')
pprint.pprint(fsa_names_sorted)

##    if name_list[time_underscore] == '0':
##        name_list[time_underscore] == '0.0'
##    fsa_names.pop(i)
##    name_join = ('_').join(name_list)
##    fsa_names.insert(0,name_join)


# print(fsa_names)
try:
    num_pts = int(input("Please enter number of time points: "))
except:
    print("Invalid integer entered, please rerun the program and input an integer")
while length_dir > num_pts or length_dir < num_pts:
    num_pts = int(input("Number of time points not consistent \
with the number of .fsa files. Please enter number of time points again: "))
x_min = int(input("Please enter the min. x value: "))
x_max = int(input("Please enter max x value: "))
while x_min > x_max:
    x_min = int(input("x value minimum is greater than x value max, please try again. x min value: "))
    x_max = int(input("Please enter max x value: "))
y_min = int(input("Please enter min y value: "))
y_max = int(input("Please enter max y value: "))
while y_min > y_max:
    y_min = int(input("y value minimum is greater than y value max, please try again. y min value: "))
    y_max = int(input("Please enter max y value: "))
##else:
###In order to get file names of the fsa plots, go to run -->
###cmd --> cd (place where file is contained)
###Ex: cd downloads --> cd --> re --> dir/b >(desiredname.txt)
###This converts the names into txt file into the folder with fsa files
###opens up text file containing the names of fsa scripts
##    file_name = input("Please enter file name (.txt format) ex: DNA.txt. Please only use if your \
##.fsa files are in the scripts folder along with the .txt file containing \
##the names of the .fsa files: ")
##    file = open(file_name,'r')
##    file.readline()


# Creates figure, axis objects for subplot
fig, ax = plt.subplots(2, num_pts // 2, sharex=True, sharey=True)

# Initialize variables for row and column
i = 0
j = 1
# Parses through each fsa file in the directory
for k in range(length_dir):
    # n = str(os.getcwd()) + '/' + fsa_dir + '/' + length_dir_name[k]
    # Takes first time point as the standard reference peak
    if k == 0:
        first_dp_split = fsa_names_sorted[k].split('_')
        time = first_dp_split[time_underscore]
        standard = SeqIO.read(fsa_names_sorted[k], 'abi')
        s_abif_key = standard.annotations['abif_raw'].keys()
        s_trace = defaultdict(list)
        s_channels = ['DATA1']
        for sc in s_channels:
            s_trace[sc] = standard.annotations['abif_raw'][sc]
        y_std_max = max(s_trace['DATA1'])
        x_std_max = s_trace['DATA1'].index(y_std_max)
        # Outputs the graph for the standard peaks
        ax[0, 0].plot(s_trace['DATA1'], color='black')
        ax[0, 0].set_title('Time: ' + time, loc='right', fontsize=8)
        ax[0, 0].set_xlim(x_min, x_max)
        ax[0, 0].set_ylim(y_min, y_max)
        continue

    # Resets the row once gets to end of row limit
    if j == num_pts // 2:
        i += 1
        j = 0
    # Gets the time for peaks
    name_split = fsa_names_sorted[k].split('_')
    time_peak = name_split[time_underscore]

    # opens up the FSA file
    record = SeqIO.read(fsa_names_sorted[k], 'abi')
    # Record returns a bunch of dictionaries. Use this line to get the dictionary
    # keys of abif_raw only
    abif_key = record.annotations['abif_raw'].keys()
    # Creates an empty list as the value in the dict
    trace = defaultdict(list)
    # DATA1 is where all the peak value is held, so only grab this dictionary key
    channels = ['DATA1']
    # Parses the channels list and returns the values for each key in dictionary
    for c in channels:
        trace[c] = record.annotations['abif_raw'][c]
    # Get the max value data
    y_peak = max(trace['DATA1'])
    # Gets the x value of the max value
    x_peak = trace['DATA1'].index(y_peak)
    # Takes difference of reference x value and time point x value
    diff = x_peak - x_std_max
    # print(diff)
    # Gets x values for vectorization purposes
    array = np.arange(1, len(trace['DATA1']) + 1)
    # Subtracts difference from array (vectorization)
    array -= diff
    # Plots the chromatogram data
    ##    for i in range(2):
    ##        for j in range(4):
    ##            if i == 0 and j == 0:
    ##                continue
    # Displays the peaks
    ax[i, j].plot(array, trace['DATA1'], color='black')
    ax[i, j].set_title('Time: ' + time_peak, loc='right', fontsize=8)
    ax[i, j].set_xlim(x_min, x_max)
    ax[i, j].set_ylim(y_min, y_max)
    # Increments column for subplot
    j += 1

##    plt.plot(array,trace['DATA1'],color='black')
#    plt.xlim(2000,3000)
##    plt.ylim(0,5000)
fig.suptitle('Chromatogram Peaks')
fig.text(0.04, 0.5, 'RFU', va='center', rotation='vertical')

plt.show()

print()
print('Now plotting 3d')
print('-------------------------------')

# !/usr/bin/env python3
from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pprint
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = plt.axes(projection='3d')
# Counter for subplot number
subplot_num = 1
# Creates a list for all the differences. Will take the largest difference to set the axes x min and x max (y min and y max for 3d scatter)
diff_list = []
# parses the directory for .fsa files
for k in range(length_dir):
    if k == 0:
        # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
        first_dp_split = fsa_names_sorted[k].split('_')
        time = first_dp_split[time_underscore]
        standard = SeqIO.read(fsa_names_sorted[k], 'abi')
        s_abif_key = standard.annotations['abif_raw'].keys()
        s_trace = defaultdict(list)
        s_channels = ['DATA1']
        for sc in s_channels:
            # s_trace['DATA1'] = y values
            s_trace[sc] = standard.annotations['abif_raw'][sc]
        x_values = s_trace['DATA1']
        y_std_max = max(x_values)
        x_std_max = x_values.index(y_std_max)
        # print(x_values[x_min:x_max+1])

        z_values = x_values[x_min:x_max + 1]
        x_values_time = [float(time)] * len(z_values)
        y_values = np.arange(x_min, x_max + 1)
        ##    print(len(x_values))
        ##    print(len(y_values))
        ##    print(len(z_values))
        # x_values = np.arange(1,len(y_values)+1)
        ##
        ##
        sc_std = ax.plot(x_values_time, y_values, z_values, alpha=0.7)
        continue

    subplot_num += 1
    name_split = fsa_names_sorted[k].split('_')
    time_peak = name_split[time_underscore]
    # opens up the FSA file
    record = SeqIO.read(fsa_names_sorted[k], 'abi')
    # Record returns a bunch of dictionaries. Use this line to get the dictionary
    # keys of abif_raw only
    abif_key = record.annotations['abif_raw'].keys()
    # Creates an empty list as the value in the dict
    trace = defaultdict(list)
    # DATA1 is where all the peak value is held, so only grab this dictionary key
    channels = ['DATA1']
    # Parses the channels list and returns the values for each key in dictionary
    for c in channels:
        trace[c] = record.annotations['abif_raw'][c]
    # Xvalues for time pts
    x_values_non_std = trace['DATA1']
    # Numpy for y values (xvalues_non_std)

    # Get the max value data
    y_peak = max(x_values_non_std)
    # Gets the x value of the max value
    x_peak = x_values_non_std.index(y_peak)
    # Takes difference of reference x value and time point x value
    diff = x_peak - x_std_max
    diff_list.append(diff)
    # print(diff)
    # X_values_non_std are really the y values on a 2d graph
    y_values_non_std = np.arange(x_min, x_max + 1) - diff
    z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
    x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)
    # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
    sc_non_std = ax.plot(x_values_time_non_std, y_values_non_std, z_values_non_std, alpha=0.7)
ax.set_ylim(x_min, x_max)
ax.set_zlim(y_min, y_max)
ax.set_xlabel('Time')
ax.set_ylabel('Data Point')
ax.set_zlabel('RFU')
# make the panes transparent
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
# ax.set_facecolor('grey')
# make the grid lines transparent
# ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
# ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
##ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)


##    #Gets x values for vectorization purposes
##    array = np.arange(1,len(trace['DATA1'])+1)
##    #Subtracts difference from array (vectorization)
##    array -= diff


fig.show()
