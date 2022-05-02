import time
import serial
import pandas as pd
from math import *
from random import *

liveData = pd.read_csv("liveData.csv", encoding='utf-8')

df = {
    "unixTime": [],
    "temp": [],
    "sal": [],
    "pH": []
}
df = pd.DataFrame(df)

latestTime = liveData.iloc[int(len(liveData.index))-1,0]

for i in range(24):
    stuff = {
        "unixTime": [round(latestTime+5-86400) + i * 3600],
        "temp": [round(liveData.iloc[int(len(liveData.index))-720+i*6:int(len(liveData.index))-720+(i+1)*6, 1].mean(), 1)],
        "sal": [round(liveData.iloc[int(len(liveData.index))-720+i*6:int(len(liveData.index))-720+(i+1)*6, 2].mean())],
        "pH": [round(liveData.iloc[int(len(liveData.index))-720+i*6:int(len(liveData.index))-720+(i+1)*6, 3].mean(), 2)]
    }
    data = pd.DataFrame(stuff)
    df = pd.concat([df, data])

df = liveData.set_index('unixTime')


print(df)
df.to_csv('historicalData.csv', index=True)