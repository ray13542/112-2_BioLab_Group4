
This project is our final project for the course of  "Biomedical Engineering Lab" in 112-2.
Our objective is to design a system that can collect electromyography signals in real-time, evaluate respiratory conditions by an machine learning model, and display them on a monitoring screen.

## Source Code
1. Data.py
    This file is used to collect data from the Arduino board and save it to a csv file.
2. 2port.ino
    This file is used to collect analog signals from the Arduino board and send it to the computer by Serial.
3. analysis.py
    This file is used to analyze the sEMG data and display the results.
4. train.ipynb
    This file is used to train the CNN model and validate the model with the test data.
5. main.py
    This file combines real-time data collection, model prediction, and display.
    It is used to demonstrate our entire system.
    