import array as arr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import pathlib

def Average(elasticity_loaded):
    return sum(elasticity_loaded) / len(elasticity_loaded)



tissueThicknessValue = 0.01783333 # m
abdominalCircumference = 0.968888889 # m
r1 = 0.136370122640148 # m
r2 = 0.154203456  # m
deviceRadius = 0.03 # m
deviceArea = np.pi*deviceRadius**2 #m^2

localFolder = str(pathlib.Path(__file__).parent.resolve())

userInput = input("Enter a file name:")

#csvFile = open(localFolder + '/IAP Device 01/' + '/data/' + userInput + '.csv', 'r')
csvFile = open(localFolder + '/data/' + userInput + '.csv', 'r')

csvReader = csv.reader(csvFile)


distance = []                                        #mm
pressureAbsolute = []                               #Pa

row = 0
for lines in csvReader:                                #no headings
    if row != 0:
        distance_reading = float(lines[1])
        pressureAbsolute_reading = float(lines[2])
        distance.append(distance_reading)
        pressureAbsolute.append(pressureAbsolute_reading*1000) #from kPa to Pa
        
    row += 1
    
distanceRef =  sum(distance[0:10])/len (distance[0:10])          #avg for initial distance
pressureAbsoluteRef = sum(pressureAbsolute[0:10])/len (pressureAbsolute[0:10])    #avg for initial absolute pressure

distance = np.array(distance ,dtype=float)
pressureAbsolute = np.array(pressureAbsolute ,dtype=float)

deformation = abs(distanceRef - distance)
deformationM = deformation/1000
pressureApplied = abs(pressureAbsolute - pressureAbsoluteRef)


        
        

strain =deformationM/(2*deviceRadius)
strain%= strain *100                                                           #%
pressureIAP=(pressureApplied*(deviceRadius**2+deformationM**2)*(r2**2-r1**2))/(4*tissueThicknessValue * deformationM *(r1**2+r2**2)-(deviceRadius**2+ deformationM**2)*(r2**2-r1**2))
stress = (pressureIAP *(r1**2+r2**2)/(r2**2-r1**2)+ pressureApplied) /1000  #kPa
force = stress * deviceArea *1000 #N
elasticity = stress/strain  #kPa

elasticity_loaded = []                               #kPa

for i in range(len(pressureApplied)):
    if pressureApplied[i] > 2000:
        elasticity_loaded.append(elasticity[i])

elasticModulus = Average(elasticity_loaded)

print("Young's modulus ="+ str(elasticModulus) + " kPa")

plt.plot(strain, stress, 'ro')
plt.xlabel('strain')
plt.ylabel('stress')
plt.show()
