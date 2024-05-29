'''
input a  csv file, there would be four columns
For the second and third columns, we do FFT and plot the result
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import os
import sys

def readdata(file, freq1, freq2):
    data = pd.read_csv(file)
    #drop the first row (header)
    data = data.drop(0)
    data = data.values
    data1 = data[:,1]
    data2 = data[:,2]
    #transform the data type to float
    data1 = data1.astype(float)
    data2 = data2.astype(float)
    #only consider 2.5 seconds data (sampling rate is 0.001s)
    data1 = data1[1000:11000]
    data2 = data2[1000:11000]

    #filter the data with a bandpass filter
    b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=1000)
    data1_bp = signal.filtfilt(b, a, data1)
    data2_bp = signal.filtfilt(b, a, data2)
    # data1_bp = data1_bp - np.min(data1_bp)
    # data2_bp = data2_bp - np.mean(data2_bp)
    #plot the original data
    # fig, ax = plt.subplots(2, 2)

    # ax[0][0].plot(data1)
    # # ax[0][0].legend(['original signal 1'])
    # ax[0][0].title.set_text('original scalenes')
    # ax[0][1].plot(data1_bp)
    # ax[0][1].set_ylim(-60, 60)
    # #limit the y-axis
    
    # # ax[0].title('Original data: signal 1')
    # ax[0][1].title.set_text('bandpass scalenes')
    # ax[1][0].plot(data2)
    # ax[1][0].title.set_text('original diaphragm')
    # ax[1][1].plot(data2_bp)
    # ax[1][1].title.set_text('bandpass diaphragm')
    # ax[1][1].set_ylim(-60, 60)
    # ax[1].title('Original data: signal 2')
    # plt.show()
    return data1_bp, data2_bp

def FFT(data1, data2):
    #FFT
    data1 = data1 - np.mean(data1)
    data2 = data2 - np.mean(data2)
    data1_fft = np.fft.fft(data1)
    data2_fft = np.fft.fft(data2)
    #keep the data in the first half
    data1_fft = data1_fft[:len(data1_fft)//2]
    data2_fft = data2_fft[:len(data2_fft)//2]
    data1_fft = np.abs(data1_fft)
    data2_fft = np.abs(data2_fft)
    #remove the DC component
    # data1_fft[0] = 0
    # data2_fft[0] = 0
    #plot the result
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(data1_fft)
    ax[0].title.set_text('FFT scalenes')
    ax[1].plot(data2_fft)
    ax[1].title.set_text('FFT diaphragm')
    plt.show()

    return data1_fft, data2_fft

def RMS(data1, data2):
    #compute the root mean square(RMS) of the signal in a 51 millisecond sliding window
    #that slides forward by one sample at a time
    RMS1 = np.zeros(len(data1)-50)
    RMS2 = np.zeros(len(data2)-50)
    for i in range(len(data1)-50):
        RMS1[i] = np.sqrt(np.mean(data1[i:i+51]**2))
        RMS2[i] = np.sqrt(np.mean(data2[i:i+51]**2))
    # fig, ax = plt.subplots(2, 1)

    # ax[0].plot(RMS1)
    # ax[0].set_ylim(0, 40)
    
    # # ax[0].title('Original data: signal 1')
    # ax[0].title.set_text('RMS scalenes')
    # ax[1].plot(RMS2)
    # ax[1].title.set_text('RMS diaphragm')
    # ax[1].set_ylim(0, 40)
    # plt.show()
    return RMS1, RMS2

def SMA_filter(data1, data2):
    #use a simple moving average(SMA) filter (which is the signal mean in a sliding window) to low-pass smooth the jagged RMSwaveform
    SMA1 = np.zeros(len(data1)-50)
    SMA2 = np.zeros(len(data2)-50)
    for i in range(len(data1)-50):
        SMA1[i] = np.mean(data1[i:i+51])
        SMA2[i] = np.mean(data2[i:i+51])
    # fig, ax = plt.subplots(2, 1)

    # ax[0].plot(SMA1)
    # # ax[0].set_ylim(0, 40)
    # ax[0].title.set_text('RMS+SMA scalenes')
    # ax[1].plot(SMA2)
    # ax[1].title.set_text('RMS+SMA diaphragm')
    # # ax[1].set_ylim(0, 40)
    return SMA1, SMA2

if __name__ == '__main__':
    # usage: python analysis.py file_path output_path
    file = sys.argv[1]
    
    freq1 = 250
    freq2 = 400
    output_path = sys.argv[2] + '/' + str(freq1) + '_' + str(freq2)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    data1, data2 = readdata(file, freq1, freq2)
    RMS1, RMS2 = RMS(data1, data2)
    SMA1, SMA2 = SMA_filter(RMS1, RMS2)
    data1_fft, data2_fft = FFT(data1, data2)
