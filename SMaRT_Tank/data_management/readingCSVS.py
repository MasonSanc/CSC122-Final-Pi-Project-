from operator import index
import time
import serial
import pandas as pd

USING_PI = False

if USING_PI:
    import RPi.GPIO
else:
    GPIO = ''

HEATER_PIN = 4
LIGHT_PIN = 5

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
arduino.reset_input_buffer()

liveData = pd.read_csv("liveData.csv", encoding='utf-8')

liveData['unixTime'] = liveData['unixTime'].astype(int)
liveData['temp'] = liveData['temp'].astype(float)
liveData['sal'] = liveData['sal'].astype(int)
liveData['pH'] = liveData['pH'].astype(float)
liveData = liveData.set_index('unixTime', drop=False)

historicData = pd.read_csv("historicalData.csv", encoding='utf-8')

historicData['unixTime'] = historicData['unixTime'].astype(int)
historicData['temp'] = historicData['temp'].astype(float)
historicData['sal'] = historicData['sal'].astype(int)
historicData['pH'] = historicData['pH'].astype(float)
historicData = historicData.set_index('unixTime', drop=False)

hourlyData = pd.read_csv("hourlyData.csv", encoding='utf-8')
dailyData = pd.read_csv("dailyData.csv", encoding='utf-8')

try:
    lastHistoricDataPoint = int(historicData.iloc[int(len(historicData.index))-1,0])
    while True:
    
        timeSinceLastHistoricPoint = int(round(time.time()) - lastHistoricDataPoint)
        if timeSinceLastHistoricPoint >= 30 and timeSinceLastHistoricPoint % 30 == 0:
            avgTemp = liveData.iloc[int(len(liveData.index))-6:, 1].mean()
            avgSal = liveData.iloc[int(len(liveData.index))-6:, 2].mean()
            avgPh = liveData.iloc[int(len(liveData.index))-6:, 3].mean()
            historicData.loc[round(time.time())] = [round(time.time()), avgTemp, avgSal, avgPh]
            if int(len(historicData.index)) > 120:
                earliestDataPoint = int(historicData.iloc[0,0])
                historicData = historicData.drop(index=earliestDataPoint, axis=index)
            print(historicData)
            lastHistoricDataPoint = int(historicData.iloc[int(len(historicData.index))-1,0])


        if arduino.in_waiting > 0 and int(time.time()) % 5 == 0:
            data = arduino.readline().decode('utf-8').rstrip()
            temp, sal, pH = data.split(",")
            temp, sal, pH = float(temp), int(sal), float(pH)
            liveData.loc[round(time.time())] = [round(time.time()), temp, sal, pH]
            print(liveData)

except KeyboardInterrupt:
    exit()
