import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
y_list = [[1.0, 0.0], [0.7767492871243694, 0.2232507128756306], [0.7346205393304761, 0.26537946066952384], [0.6831905961376994, 0.3168094038623006], [0.6606518518518518, 0.3393481481481481], [0.6313103992748432, 0.3686896007251568], [0.6223647183650874, 0.37763528163491256], [0.614149790038803, 0.38585020996119707], [0.6204573757500284, 0.3795426242499717], [0.6225351419216661, 0.37746485807833385], [0.5971364450862024, 0.4028635549137976], [0.5899561620589691, 0.4100438379410309], [0.5765158806544755, 0.42348411934552455], [0.5776028899496839, 0.4223971100503161], [0.5743400211193241, 0.4256599788806758], [0.5713668410279736, 0.42863315897202636], [0.5817053651691552, 0.4182946348308448], [0.566664701605455, 0.433335298394545], [0.5607592791367719, 0.4392407208632281], [0.5506682184853714, 0.44933178151462855]]
x = ['27mer','28mer']
time = [0.0, 0.0025, 0.004, 0.006, 0.008, 0.01, 0.012, 0.015, 0.018, 0.021, 0.025, 0.03, 0.04, 0.05, 0.065, 0.08, 0.1, 0.15, 0.2, 0.4]
#for i in range(len(y_list)-1):
f,axarr = plt.subplots(len(y_list)//2 ,2,sharex=True,sharey=True)
f.suptitle('Fractional Area vs. Size')
##axarr[0].bar(x,y_list[0],width=0.1)
##axarr[0].set_title('0',loc='right')
#axarr[0].bar(x,y_list[0],width=0.1)

#axarr[0,0].bar(x,y_list[0],width=0.1)
##            axarr[i,j].set_title('Time: ' + str(time[i]),loc='right',fontsize=8)
##for i in range(2):
##    if i == 1:
##        for j in range(int(len(y_list)/2),len(y_list)):
##            axarr[i,j].bar(x,y_list[j],width=0.1)
##            axarr[i,j].set_title('Time: ' + str(time[i]),loc='right',fontsize=8)
##    for j in range(int(len(y_list)/2)):
##        axarr[i,j].bar(x,y_list[j],width=0.1)
##        axarr[i,j].set_title('Time: ' + str(time[i]),loc='right',fontsize=8)
        
##count = 0
##while i < len(y_list)/2:
##    axarr[count,i].bar(x,y_list[i],width=0.1)
##    axarr[count,i].set_title('Time: ' + str(time[i]),loc='right',fontsize=8)
##    count += 1
##    i+=1
##
print(y_list[19])
count = 0
for i in range(2):
    for j in range(len(time)//2):
        axarr[j,i].bar(x,y_list[count],width=0.1)
        axarr[j,i].set_title('Time: ' + str(time[count]),loc='right',fontsize=8)
        print(count)
        count+=1
        
    

f.text(0.04,0.5,'Fractional Area', va='center', rotation='vertical')
#plt.figure(1)
#plt.bar(x,y_list[1],width=0.1)

plt.subplots_adjust(hspace=0.4)
#plt.xticks(np.arange(len(x)),x)
plt.xlabel('Size')
#plt.ylabel('Fractional Area',labelpad=20)
plt.show()
    

### CREATE DATA
##bar_heights = [1, 4]
##bar_labels = ['alpha', 'beta', 'gamma', 'delta']
##bar_x_positions = [0,1]
##
### PLOT A SIMPLE BAR CHART
##plt.bar(bar_x_positions, bar_heights)
##plt.show()
