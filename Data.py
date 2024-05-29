import serial
import re
import csv
import serial.tools.list_ports
import time

# print all available COM ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port)

# 連接到 Arduino
COM_PORT = 'COM9'
BAUD_RATES = 115200
arduinoSerial = serial.Serial(COM_PORT, BAUD_RATES)

time_arr = []
data1 = []
data2 = []
data_now = 1

# 設定量測時間
measurement_time = 15 # seconds
# 設定呼吸類型
breath_class = 2

with open('3-4.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['time', 'diaphragm', 'scalenes', 'class'])
    start_time = time.time()
    while time.time() - start_time < measurement_time:
        if arduinoSerial.in_waiting:
            byte = arduinoSerial.readline()
            byte_str = str(byte)

            # skip when read the wrong form
            if not byte_str[2].isdigit(): continue        

            # find the num pair
            num = re.findall('\d+', byte_str)

            # append data
            time_arr.append(time.time() - start_time)
            if len(num) !=2: 
                print('wrong input!')
                continue
            print(num[0], num[1])
            data1.append(int(num[0]))
            data2.append(int(num[1]))
            
    for a1, a2, a3 in zip(time_arr, data1, data2):
        csv_writer.writerow([a1, a2, a3, breath_class])
            


