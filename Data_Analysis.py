import pandas as pd
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import csv

datas = pd.read_csv('template.csv')
t = datas.iloc[:, 1].values
deformation = datas.iloc[:, 3].values
pressure = datas.iloc[:, 5].values
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Setting standard filter requirements.
order = 1
fs = 150
cutoff = 3

b, a = butter_lowpass(cutoff, fs, order)
# Creating the data for filteration
T = 5.0         # value taken in seconds
n = int(T * fs) # indicates total samples

# Filtering and plotting
filtered_deformation = butter_lowpass_filter(deformation, cutoff, fs, order)

df = pd.DataFrame(filtered_deformation)
df.to_csv('filteredeformation.csv')



plt.subplot(2, 1, 1)
plt.plot(t, pressure, 'b-', linewidth=1, label='net pressure')
plt.plot(t, deformation, 'g-', label='data')
plt.plot(t, filtered_deformation, 'r-', linewidth=1, label='filtered deformation data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
stress = []
strain = []

for i in range(len(pressure)):
    if pressure[i] > 0.2:
        stress_value = (pressure[i] * 1000) / (1 / (0.001 * filtered_deformation[i]) + 1 / 0.03)
        stress.append(stress_value)
        strain_value = (filtered_deformation[i] * 0.001) / 0.03
        strain.append(strain_value)
    else:
        stress.append(0)
        strain.append(0)
#for i in range(len(stress)-1):
   # if stress[i] == 0 and stress[i+1] != 0:
    #    stress1 = stress[i:]
  #      strain1 = strain[i:]
  #      break
#for i in range(len(stress1)-1):
    #if stress1[i] == 0 and stress1[i+1] != 0 and i != 0:
   ##     stress2 = stress1[i:]
     #   strain2 = strain1[i:]
     ##   break
#for i in range(len(stress2)-1):
  #  if stress2[i] == 0 and stress2[i+1] != 0 and i != 0:
      #  stress3 = stress2[i:]
      #  strain3 = strain2[i:]
      #  break

#for i in range(len(stress1)-1):
  #  if stress1[i] == 0 and stress1[i+1] != 0 and i != 0:
  #      stress1 = stress1[:i]
    #    strain1 = strain1[:i]
    #    break
#for i in range(len(stress2)-1):
 #   if stress2[i] == 0 and stress2[i+1] != 0 and i != 0:
 #       stress2 = stress2[:i]
 #       strain2 = strain2[:i]
 #       break
#linstress1 = []
#linstrain1 = []
#linstress2 = []
#linstrain2 = []
#linstress3 = []
#linstrain3 = []##

#for i in range(len(stress1)-1):
   # if stress1[i] < stress1[i+1]:
       # linstress1.append(stress1[i])
       # linstrain1.append(strain1[i])

#for i in range(len(stress2)-1):
   # if stress2[i] < stress2[i+1]:
     #   linstress2.append(stress2[i])
      #  linstrain2.append(strain2[i])

#for i in range(len(stress3)-1):
    #if stress3[i] < stress3[i+1]:
     #   linstress3.append(stress3[i])
     #   linstrain3.append(strain3[i])


#print(linstress1)
#linzone1 = stats.linregress(linstrain1, linstress1)
#linzone2 = stats.linregress(linstrain2, linstress2)
#linzone3 = stats.linregress(linstrain3, linstress3)


plt.plot(strain, stress, 'g-', linewidth=1)
#plt.plot(strain2, stress2, 'b-', linewidth=1, label='stress2 Elastic Mod: '+str(linzone2.slope))
#plt.plot(strain3, stress3, 'r-', linewidth=1, label='stress3 Elastic Mod: '+str(linzone3.slope))
plt.xlabel('Strain')
#print(linzone1.slope)
#print(linzone2.slope)
#print(linzone3.slope)

plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show()

