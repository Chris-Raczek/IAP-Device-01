#24:6F:28:1B:63:DA

import serial as serial
import csv
import pathlib
from pathlib import Path




class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)
ComPort = "COM"+input("COM Port #:")
ser = serial.Serial(ComPort, 9600)
rl = ReadLine(ser)

localFolder = str(pathlib.Path(__file__).parent.resolve())
pathlib.Path(localFolder + '/data').mkdir(parents=True, exist_ok=True)
userInput = input("Enter a file name:")
csvFile = open(localFolder + '/data/' + userInput + '.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(
    ['Time', 'Tissue Displacement', 'Pressure', 'Temperature', 'Piston Displacement', 'Opening Diameter',
     'Battery Voltage', 'Charging', 'deformation', 'pressureApplied', 'IAP', 'stress', 'force', 'strain',
     'elasticity'])

while True:
    output = rl.readline().decode("utf-8")
    csvWriter.writerow(output.split()[1:])
    output = output.split()[1:]
    print(output)

