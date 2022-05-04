from operator import index
import time
import serial
import pandas as pd

def USING_PI():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

if USING_PI():
    import RPi.GPIO as GPIO
else:
    GPIO = ''

GPIO.setmode(GPIO.BCM)
HEATER_PIN = 4
LIGHT_PIN = 5
GPIO.setup(HEATER_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)

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

hourlyData['unixTime'] = hourlyData['unixTime'].astype(int)
hourlyData['temp'] = hourlyData['temp'].astype(float)
hourlyData['sal'] = hourlyData['sal'].astype(int)
hourlyData['pH'] = hourlyData['pH'].astype(float)
hourlyData = hourlyData.set_index('unixTime', drop=False)

dailyData = pd.read_csv("dailyData.csv", encoding='utf-8')

dailyData['unixTime'] = dailyData['unixTime'].astype(int)
dailyData['temp'] = dailyData['temp'].astype(float)
dailyData['sal'] = dailyData['sal'].astype(int)
dailyData['pH'] = dailyData['pH'].astype(float)
dailyData = dailyData.set_index('unixTime', drop=False)

light_mode = 0
GPIO.output(LIGHT_PIN, GPIO.LOW)

try:
    lastHistoricDataPoint = int(historicData.iloc[int(len(historicData.index))-1,0])
    lastHourlyDataPoint = int(hourlyData.iloc[int(len(hourlyData.index))-1,0])
    lastDailyDataPoint = int(dailyData.iloc[int(len(dailyData.index))-1,0])
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
            lastHistoricDataPoint = int(historicData.iloc[int(len(historicData.index))-1,0])

        timeSinceLastHourlyDataPoint = int(round(time.time()) - lastHourlyDataPoint)
        if timeSinceLastHourlyDataPoint >= 3600 and timeSinceLastHourlyDataPoint % 3600 == 0:
            avgTemp = liveData.iloc[int(len(liveData.index))-720:, 1].mean()
            avgSal = liveData.iloc[int(len(liveData.index))-720:, 2].mean()
            avgPh = liveData.iloc[int(len(liveData.index))-720:, 3].mean()
            hourlyData.loc[round(time.time)] = [round(time.time()), avgTemp, avgSal, avgPh]
            if int(len(hourlyData.index)) > 120:
                earliestDataPoint = int(hourlyData.iloc[0,0])
                hourlyData = hourlyData.drop(index=earliestDataPoint, axis=index)
            lastHourlyDataPoint = int(hourlyData.iloc[int(len(hourlyData.index))-1,0])

        timeSinceLastDailyDataPoint = int(round(time.time()) - lastDailyDataPoint)
        if timeSinceLastDailyDataPoint >= 86400 and (timeSinceLastDailyDataPoint - 18000) % 86400 == 0:
            avgTemp = liveData.iloc[int(len(liveData.index))-86400:, 1].mean()
            avgSal = liveData.iloc[int(len(liveData.index))-86400:, 2].mean()
            avgPh = liveData.iloc[int(len(liveData.index))-86400:, 3].mean()
            dailyData.loc[round(time.time())] = [round(time.time()), avgTemp, avgSal, avgPh]
            if int(len(dailyData.index)) > 120:
                earliestDataPoint = int(dailyData.iloc[0,0])
                dailyData = dailyData.drop(index=earliestDataPoint, axis=index)
            lastDailyDataPoint = int(dailyData.iloc[int(len(dailyData.index))-1,0])

        if arduino.in_waiting > 0 and int(time.time()) % 5 == 0:
            data = arduino.readline().decode('utf-8').rstrip()
            temp, sal, pH = data.split(",")
            temp, sal, pH = float(temp), int(sal), float(pH)
            liveData.loc[round(time.time())] = [round(time.time()), temp, sal, pH]

        if int(time.strftime(time.localtime(),"%M")) == 5 and lightLastChanged - round(time.time()) >= 300:
            if light_mode == 0:
                light_mode = 1
                GPIO.output(LIGHT_PIN, GPIO.HIGH)
                lightLastChanged = round(time.time())
            else:
                light_mode = 0
                GPIO.output(LIGHT_PIN, GPIO.LOW)
                lightLastChanged = round(time.time())

        

except KeyboardInterrupt:
    GPIO.cleanup()
    exit()
