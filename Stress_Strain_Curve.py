import matplotlib.pyplot as plt
from scipy import stats
from scipy.integrate import simps
import csv
import pathlib
import numpy as np

localFolder = str(pathlib.Path(__file__).parent.resolve())

userInput = input("Enter a folder name:")

csvFile = open(localFolder + '/Testing_Day_2/' + userInput +'/Test1/'+'Test1.Stop.csv', 'r')

csvReader = csv.reader(csvFile)
thickness1 = float(input('thickness value 1: '))
thickness2 = float(input('thickness value 2: '))
thickness3 = float(input('thickness value 3: '))

width1 = float(input('width value 1: '))
width2 = float(input('width value 2: '))
width3 = float(input('width value 3: '))

average_thickness = (thickness3+thickness2+thickness1)/3
average_width = (width3+width2+width1)/3
area = average_width*average_thickness
stress = []
strain = []
force = []
displacement = []
gauge = 50
row = 0
for lines in csvReader:
    if row != 0:
        stress_calculation = float(lines[8])/area
        strain_calculation = float(lines[9])/gauge
        stress.append(stress_calculation)
        strain.append(strain_calculation)
        force.append(float(lines[8]))
        displacement.append(float(lines[9]))

    row += 1
    
    
loading = []
load_displacement = []
unloading = []
unload_displacement = []
for i in range(len(displacement)-1):
    if (displacement[i] - displacement[i+1]) < 0:
        loading.append(force[i])
        load_displacement.append(displacement[i])
    else:
        unloading.append(force[i])
        unload_displacement.append(displacement[i])






#force = np.array(force)
displacement = np.array(displacement)

linear_zone = stats.linregress(strain, stress)
slope = float(linear_zone.slope)
intercept = float(linear_zone.intercept)
linear_stress = []

for i in strain:
    lin_calc = slope*i + intercept
    linear_stress.append(lin_calc)

#hysteresis = simps(force, dx=0.1)

#print(hysteresis)
area = np.trapz(y=loading, x=load_displacement)
area2 = np.trapz(y=unloading, x=unload_displacement)
hysteresis = area-area2
print(hysteresis)
plt.subplot(2, 1, 1)
plt.plot(strain, stress)
plt.plot(strain, linear_stress, 'g-', label=('linear regression: '+str(slope*1000)+' kPa'))

plt.xlabel('Strain')
plt.ylabel('Stress [MPa]')
plt.grid()
plt.legend()

plt.title('Stress v Strain')

plt.subplot(2, 1, 2)
plt.plot(load_displacement, loading)
plt.plot(unload_displacement, unloading, '-g', label=('hysteresis= '+str(hysteresis)))

plt.xlabel('Displacement [mm]')
plt.ylabel('Force [N]')
plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)

plt.show()

