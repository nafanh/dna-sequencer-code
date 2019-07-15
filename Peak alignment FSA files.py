#! python3
from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
#In order to get file names of the fsa plots, go to run -->
#cmd --> cd (place where file is contained)
#Ex: cd downloads --> cd --> re --> dir/b >(desiredname.txt)
#This converts the names into txt file into the folder with fsa files

#In order to get the text file name from the folder

folder_check = input("If your .fsa files are in a folder, press 'y' to continue, else press 'n': ")
if folder_check == 'y' or folder_check == 'Y':
    txt_name = ''
    fsa_dir = input('Please enter the name of the folder with the .fsa files: ')
    for f_name in os.listdir(fsa_dir + '/'):
        if f_name.endswith('.txt'):
            txt_name = f_name
    file_name = txt_name
else:
    #opens up text file containing the names of fsa scripts
    file_name = input("Please enter file name (.txt format) ex: DNA.txt. Please only use if your \
.fsa files are in the scripts folder along with the .txt file containing \
the names of the .fsa files: ")
file = open(file_name,'r')
file.readline()
#Gets the x values
#a = [x for x in range(len(trace['DATA1'])+1)]
#for vectorization purposes
#array = np.arange(1,len(trace['DATA1'])+1)
#Parses each line of the text file

#Get the max value data
#max(trace['DATA1'])
#Gets the x value of the max value
#trace['DATA1'].index(max(trace['DATA1']))

#Prompts user for number of time points and the y/x min and max

#Checks how many fsa files are in the text file. If not equal to the number
#of time points entered, then requests user to enter number of time points again
count = 0
for fsa_file in file:
    fsa_file = fsa_file.rstrip('\n')
    if fsa_file.endswith('.fsa'):
        count += 1
num_pts = int(input("Please enter number of time points: "))
while count > num_pts or count < num_pts:
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
file.close()

#Opens file again because it already parsed through all lines the first time
file = open(file_name,'r')
file.readline()
#Creates figure, axis objects for subplot
fig,ax = plt.subplots(2,num_pts//2,sharex=True,sharey=True)
count = 1
#Sets the data points of the first time point as the standard
first_dp = file.readline().rstrip('\n')
#Gets time point from description name
#Time point is always after the third underscore
first_dp_split = first_dp.split('_')
time = first_dp_split[2]
#Reads in the standard peak
standard = SeqIO.read(first_dp,'abi')
#Gets the keys from annotations dictionary
s_abif_key = standard.annotations['abif_raw'].keys()
#Initializes empty list values for dictionary to prevent keyerror
s_trace = defaultdict(list)
s_channels = ['DATA1']
#Adds raw chromatogram data to the dictionary
for sc in s_channels:
    s_trace[sc] = standard.annotations['abif_raw'][sc]
#Gets the y value for peak of reference peak
y_std_max = max(s_trace['DATA1'])
x_std_max = s_trace['DATA1'].index(y_std_max)
##plt.plot(s_trace['DATA1'],color='black')
##plt.xlim(2500,2700)
##plt.show()
#Outputs the graph for the standard peaks
ax[0,0].plot(s_trace['DATA1'],color='black')
ax[0,0].set_title('Time: ' + time, loc='right',fontsize=8)
ax[0,0].set_xlim(x_min,x_max)
ax[0,0].set_ylim(y_min,y_max)

#Initialize variables for row and column
i = 0
j = 1
for line in file:
    #Resets the row once gets to end of row limit
    if j == num_pts//2:
        i+=1
        j = 0
    name = line.rstrip('\n')
    #Ends the loop if empty line
    if not name:
        break
    #Gets the time for peaks
    name_split = name.split('_')
    time_peak = name_split[2]
    # print(name_split)
    # print(time_peak)
    #opens up the FSA file
    record = SeqIO.read(name,'abi')
    #Record returns a bunch of dictionaries. Use this line to get the dictionary
    #keys of abif_raw only
    abif_key = record.annotations['abif_raw'].keys()
    #Creates an empty list as the value in the dict
    trace = defaultdict(list)
    #DATA1 is where all the peak value is held, so only grab this dictionary key
    channels = ['DATA1']
    #Parses the channels list and returns the values for each key in dictionary
    for c in channels:
        trace[c] = record.annotations['abif_raw'][c]
    #Get the max value data
    y_peak = max(trace['DATA1'])
    #Gets the x value of the max value
    x_peak = trace['DATA1'].index(y_peak)
    #Takes difference of reference x value and time point x value
    diff = x_peak - x_std_max
    #print(diff)
    #Gets x values for vectorization purposes
    array = np.arange(1,len(trace['DATA1'])+1)
    #Subtracts difference from array (vectorization)
    array -= diff
    #Plots the chromatogram data
##    for i in range(2):
##        for j in range(4):
##            if i == 0 and j == 0:
##                continue
    #Displays the peaks
    ax[i,j].plot(array,trace['DATA1'],color='black')
    ax[i,j].set_title('Time: ' + time_peak, loc='right',fontsize=8)
    ax[i,j].set_xlim(x_min,x_max)
    ax[i,j].set_ylim(y_min,y_max)
    #Increments column for subplot
    j+=1

##    plt.plot(array,trace['DATA1'],color='black')
#    plt.xlim(2000,3000)
##    plt.ylim(0,5000)
fig.suptitle('Chromatogram Peaks')
fig.text(0.04,0.5,'RFU', va='center', rotation='vertical')

plt.show()
file.close()
