#! python3
from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import gui
#Program works so you don't have to use the cmd line dir>/b

#In order to get the text file name from the folder
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

#Checks how many fsa files are in the directory. If not equal to the number
#of time points entered, then requests user to enter number of time points again

#Try this for Gui
folder_check = gui.is_folder
#folder_check = input("If your .fsa files are in a folder, press 'y' to continue, else press 'n': ")
if folder_check == 'y' or folder_check == 'Y':

    #Try this for Gui
    fsa_dir = gui.f_name
    #fsa_dir = input('Please enter the name of the folder with the .fsa files: ')
    fsa_dir = os.getcwd() + '\\' + fsa_dir 
    fsa_dir_list = os.listdir(fsa_dir)
    #print(fsa_dir)
    fsa_names = [x for x in fsa_dir_list if x.endswith('.fsa')]
    length_dir = len(fsa_names)
    #num_pts = int(input("Please enter number of time points: "))
    #Try for GUI
    num_pts = gui.time
    while length_dir > num_pts or length_dir < num_pts:
        num_pts = int(input("Number of time points not consistent \
    with the number of .fsa files. Please enter number of time points again: "))

    #Try for GUI
    x_min = gui.x_min
    x_max = gui.x_max
##    x_min = int(input("Please enter the min. x value: "))
##    x_max = int(input("Please enter max x value: "))
    while x_min > x_max:
        x_min = int(input("x value minimum is greater than x value max, please try again. x min value: "))
        x_max = int(input("Please enter max x value: "))

    #Try for GUI
    y_min = gui.y_min
    y_max = gui.y_max
##    y_min = int(input("Please enter min y value: "))
##    y_max = int(input("Please enter max y value: "))
    while y_min > y_max:
        y_min = int(input("y value minimum is greater than y value max, please try again. y min value: "))
        y_max = int(input("Please enter max y value: "))
else:
#In order to get file names of the fsa plots, go to run -->
#cmd --> cd (place where file is contained)
#Ex: cd downloads --> cd --> re --> dir/b >(desiredname.txt)
#This converts the names into txt file into the folder with fsa files
#opens up text file containing the names of fsa scripts
    file_name = input("Please enter file name (.txt format) ex: DNA.txt. Please only use if your \
.fsa files are in the scripts folder along with the .txt file containing \
the names of the .fsa files: ")
    file = open(file_name,'r')
    file.readline()


#Creates figure, axis objects for subplot
fig,ax = plt.subplots(2,num_pts//2,sharex=True,sharey=True)


#Initialize variables for row and column
i = 0
j = 1
    
#Parses through each fsa file in the directory
for k in range(length_dir):
    #Takes first time point as the standard reference peak
    if k == 0:
        first_dp_split = fsa_names[0].split('_')
        time = first_dp_split[2]
        standard = SeqIO.read(fsa_names[0],'abi')
        s_abif_key = standard.annotations['abif_raw'].keys()
        s_trace = defaultdict(list)
        s_channels = ['DATA1']
        for sc in s_channels:
            s_trace[sc] = standard.annotations['abif_raw'][sc]
        y_std_max = max(s_trace['DATA1'])
        x_std_max = s_trace['DATA1'].index(y_std_max)
        #Outputs the graph for the standard peaks
        ax[0,0].plot(s_trace['DATA1'],color='black')
        ax[0,0].set_title('Time: ' + time, loc='right',fontsize=8)
        ax[0,0].set_xlim(x_min,x_max)
        ax[0,0].set_ylim(y_min,y_max)
        continue
        
  
    #Resets the row once gets to end of row limit
    if j == num_pts//2:
        i+=1
        j = 0
    #Gets the time for peaks
    name_split = fsa_names[k].split('_')
    time_peak = name_split[2]

    #opens up the FSA file
    record = SeqIO.read(fsa_names[k],'abi')
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







