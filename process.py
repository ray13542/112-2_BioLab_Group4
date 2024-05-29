# Description: This file contains the function to process the data from the csv file.
import numpy as np
import pandas as pd
from scipy import signal

def process_csv(file_path, freq1=20, freq2=450, fs=1000, process_method='bp'):
    """
    read the csv file and process the data
    :param file_path: the path of the csv file
    :param freq1: the lower bound of the bandpass filter
    :param freq2: the upper bound of the bandpass filter
    :param fs: the sampling rate
    :return: the processed data
    """

    df = pd.read_csv(file_path)
    
    data1 = df.iloc[:, 1]
    data2 = df.iloc[:, 2]
    if process_method == 'raw_data':
        processed_df = pd.DataFrame({
            'time': df.iloc[:, 0],
            'EMG1': data1,
            'EMG2': data2,
            'class': df.iloc[:, 3]
        })
    elif process_method == 'bp':
        # filter the data with a bandpass filter
        b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=fs)
        data1 = signal.filtfilt(b, a, data1)
        data2 = signal.filtfilt(b, a, data2)
        processed_df = pd.DataFrame({
        'time': df.iloc[:, 0],
        'EMG1': data1,
        'EMG2': data2,
        'class': df.iloc[:, 3]
    })
    elif process_method == 'sma':
        # SMA
        SMA1 = np.zeros(len(data1) - 50)
        SMA2 = np.zeros(len(data2) - 50)
        for i in range(len(data1) - 50):
            SMA1[i] = np.mean(data1[i:i + 51])
            SMA2[i] = np.mean(data2[i:i + 51])

        processed_df = pd.DataFrame({
            'time': df.iloc[50:, 0],
            'SMA1': SMA1,
            'SMA2': SMA2,
            'class': df.iloc[50:, 3]
        })
    elif process_method == 'bp+rms':
        # filter the data with a bandpass filter
        b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=fs)
        data1_bp = signal.filtfilt(b, a, data1)
        data2_bp = signal.filtfilt(b, a, data2)

        # calculate the RMS
        RMS1 = np.zeros(len(data1_bp)-50)
        RMS2 = np.zeros(len(data2_bp)-50)
        
        for i in range(len(data1_bp)-50):
            RMS1[i] = np.sqrt(np.mean(data1_bp[i:i+51]**2))
            RMS2[i] = np.sqrt(np.mean(data2_bp[i:i+51]**2))
        
        processed_df = pd.DataFrame({
            'time': df.iloc[50:, 0],
            'EMG1': RMS1,
            'EMG2': RMS2,
            'class': df.iloc[50:, 3]
        })
    elif process_method == 'bp+sma':
        # filter the data with a bandpass filter
        b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=fs)
        data1_bp = signal.filtfilt(b, a, data1)
        data2_bp = signal.filtfilt(b, a, data2)
        
        # SMA
        SMA1 = np.zeros(len(data1_bp) - 50)
        SMA2 = np.zeros(len(data2_bp) - 50)
        for i in range(len(data1_bp) - 50):
            SMA1[i] = np.mean(data1_bp[i:i + 51])
            SMA2[i] = np.mean(data2_bp[i:i + 51])

        processed_df = pd.DataFrame({
            'time': df.iloc[50:, 0],
            'SMA1': SMA1,
            'SMA2': SMA2,
            'class': df.iloc[50:, 3]
        })
    elif process_method == 'bp+rms+sma':
        # filter the data with a bandpass filter
        b, a = signal.butter(4, [freq1, freq2], 'bandpass', fs=fs)
        data1_bp = signal.filtfilt(b, a, data1)
        data2_bp = signal.filtfilt(b, a, data2)

        # calculate the RMS
        RMS1 = np.zeros(len(data1_bp) - 50)
        RMS2 = np.zeros(len(data2_bp) - 50)

        for i in range(len(data1_bp) - 50):
            RMS1[i] = np.sqrt(np.mean(data1_bp[i:i + 51] ** 2))
            RMS2[i] = np.sqrt(np.mean(data2_bp[i:i + 51] ** 2))

        # SMA
        SMA1 = np.zeros(len(RMS1) - 50)
        SMA2 = np.zeros(len(RMS2) - 50)
        for i in range(len(RMS1) - 50):
            SMA1[i] = np.mean(RMS1[i:i + 51])
            SMA2[i] = np.mean(RMS2[i:i + 51])

        processed_df = pd.DataFrame({
            'time': df.iloc[100:, 0],
            'SMA1': SMA1,
            'SMA2': SMA2,
            'class': df.iloc[100:, 3]
        })
    
    return processed_df

def sliding_window(data, window_size, stride):
    """
    Create sliding windows of the data
    :param data: the data to be windowed
    :param window_size: the size of the window
    :param stride: the stride of the window
    :return: the windowed data and the corresponding labels
    """
    windowed_data = []
    labels = []

    for i in range(0, len(data) - window_size + 1, stride):
        windowed = data.iloc[i:i + window_size, :-1].values  # Exclude label column and convert to NumPy array
        label_window = data.iloc[i:i + window_size, -1]  # Get all labels in the window
        if len(label_window.unique()) == 1:  # Check if all labels in the window are the same
            windowed_data.append(windowed)
            labels.append(label_window.iloc[0])  # Use the first label as the label for the window

    return np.array(windowed_data), np.array(labels)