from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#opens up text file containing the names of fsa scripts
file = open('files.txt','r')
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

#Sets the data points of the first time point as the standard
first_dp = file.readline().rstrip('\n')
standard = SeqIO.read(first_dp,'abi')
s_abif_key = standard.annotations['abif_raw'].keys()
s_trace = defaultdict(list)
s_channels = ['DATA1']
for sc in s_channels:
    s_trace[sc] = standard.annotations['abif_raw'][sc]
#Gets the y value for peak of reference peak
y_std_max = max(s_trace['DATA1'])
x_std_max = s_trace['DATA1'].index(y_std_max)
plt.plot(s_trace['DATA1'],color='black')
plt.xlim(2500,2700)
plt.show()

for line in file:
    name = line.rstrip('\n')
    #Ends the loop if empty line
    if not name:
        break
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
    print(diff)
    #Gets x values for vectorization purposes
    array = np.arange(1,len(trace['DATA1'])+1)
    #Subtracts difference from array (vectorization)
    array -= diff
    #Plots the chromatogram data
    plt.plot(array,trace['DATA1'],color='black')
    plt.xlim(2500,2700)
    plt.ylim(0,5000)
    plt.show()
file.close()
