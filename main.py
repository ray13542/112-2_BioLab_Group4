import serial
import re
import csv
import serial.tools.list_ports
import time
import numpy as np
from tensorflow import keras
from scipy import signal
import tkinter as tk

# Load your trained machine learning modelimport os
models_name = 'EMG_classification_newdata_raw_data_0_0.keras'  # 'EMG_classification_bp+SMA_100_400.keras', 'EMG_classification_raw_data_1_2.keras'
model = keras.models.load_model('./models/'+models_name)


# 連接到 Arduino
COM_PORT = 'COM9'
BAUD_RATES = 115200
arduinoSerial = serial.Serial(COM_PORT, BAUD_RATES)

time_arr = []
data1 = []
data2 = []

# Parameters
freq1 = 100
freq2 = 400
window_size = 3000

def process_data(data1, data2):
    # Filter the data with a bandpass filter
    b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=1000)
    data1_bp = signal.filtfilt(b, a, data1)
    data2_bp = signal.filtfilt(b, a, data2)
    
    # SMA
    SMA1 = np.zeros(len(data1_bp) - 50)
    SMA2 = np.zeros(len(data2_bp) - 50)
    for i in range(len(data1_bp) - 50):
        SMA1[i] = np.mean(data1_bp[i:i + 51])
        SMA2[i] = np.mean(data2_bp[i:i + 51])
    window_data = np.array([SMA1, SMA2])
    return window_data

class BreathingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Breathing Monitor")
        self.root.geometry("600x600")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        self.title_label = tk.Label(root, text="呼吸狀態評估", font=("Arial", 24), bg="black", fg="white")
        self.title_label.pack(pady=10)

        self.normal_block = tk.Label(root, text="正常呼吸", width=20, height=10, bg="white")
        self.heavy_block = tk.Label(root, text="劇烈呼吸", width=20, height=10, bg="white")
        self.cough_block = tk.Label(root, text="咳嗽", width=20, height=10, bg="white")

        self.normal_block.pack(pady=5)
        self.heavy_block.pack(pady=5)
        self.cough_block.pack(pady=5)

    def update_display(self, prediction):
        # Reset all blocks to white
        self.normal_block.config(bg="white")
        self.heavy_block.config(bg="white")
        self.cough_block.config(bg="white")

        # Update the block color based on the prediction
        if prediction == 0:
            self.normal_block.config(bg="green")
        elif prediction == 1:
            self.heavy_block.config(bg="red")
        elif prediction == 2:
            self.cough_block.config(bg="yellow")

root = tk.Tk()
app = BreathingApp(root)

start=time.time()
while True:
    if arduinoSerial.in_waiting:
        byte = arduinoSerial.readline()
        byte_str = str(byte)
        # skip when read the wrong form
        if not byte_str[2].isdigit(): continue        

        # find the num pair
        num = re.findall('\d+', byte_str)

        # append data
        if len(num) !=2: 
            print('wrong input!')
            continue
        #print(num[0], num[1])
        data1.append(int(num[0]))
        data2.append(int(num[1]))

        if len(data1)==3000: #3000 for raw, 3050 for bp+sma
            print(time.time()-start)
            #processed_data = np.array([np.transpose(process_data(data1, data2))])
            processed_data = np.array([np.transpose([data1, data2])])
            #print(processed_data.shape)
            prediction = model.predict(processed_data)
            predict_max = np.argmax(prediction, axis=1)
            print(f'prediction: {prediction}')
            print(time.time()-start)
            app.update_display(predict_max)
            root.update()
            # root.after(1000)  # wait for 1 second before changing to next prediction



            data1 = []
            data2 = []

        


            


