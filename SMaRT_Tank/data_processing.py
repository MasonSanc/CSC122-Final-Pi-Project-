from operator import index
import time
import serial
import pandas as pd

class Data():

    SAVED_DATA_FILE = './data_management/liveData.csv'
    SECONDLY_DATA_FILE = './data_management/historicalData.csv'
    HOURLY_DATA_FILE = './data_management/hourlyData.csv'
    DAILY_DATA_FILE = './data_management/dailyData.csv'
    
    def __init__(self):

        self.saved_data = pd.read_csv(self.SAVED_DATA_FILE, encoding='utf-8')

        self.saved_data['unixTime'] = self.saved_data['unixTime'].astype(int)
        self.saved_data['temp'] = self.saved_data['temp'].astype(float)
        self.saved_data['sal'] = self.saved_data['sal'].astype(int)
        self.saved_data['pH'] = self.saved_data['pH'].astype(float)
        self.saved_data = self.saved_data.set_index('unixTime', drop=False)

        self.second_data = pd.read_csv(self.SECONDLY_DATA_FILE, encoding='utf-8')

        self.second_data['unixTime'] = self.second_data['unixTime'].astype(int)
        self.second_data['temp'] = self.second_data['temp'].astype(float)
        self.second_data['sal'] = self.second_data['sal'].astype(int)
        self.second_data['pH'] = self.second_data['pH'].astype(float)
        self.second_data = self.second_data.set_index('unixTime', drop=False)

        self.hourly_data = pd.read_csv(self.HOURLY_DATA_FILE, encoding='utf-8')

        self.hourly_data['unixTime'] = self.hourly_data['unixTime'].astype(int)
        self.hourly_data['temp'] = self.hourly_data['temp'].astype(float)
        self.hourly_data['sal'] = self.hourly_data['sal'].astype(int)
        self.hourly_data['pH'] = self.hourly_data['pH'].astype(float)
        self.hourly_data = self.hourly_data.set_index('unixTime', drop=False)

        self.daily_data =  pd.read_csv(self.DAILY_DATA_FILE, encoding='utf-8')

        self.daily_data['unixTime'] = self.daily_data['unixTime'].astype(int)
        self.daily_data['temp'] = self.daily_data['temp'].astype(float)
        self.daily_data['sal'] = self.daily_data['sal'].astype(int)
        self.daily_data['pH'] = self.daily_data['pH'].astype(float)
        self.daily_data = self.daily_data.set_index('unixTime', drop=False)

        self.last_secondly_data_point = int(self.second_data.iloc[int(len(self.second_data.index))-1,0])
        self.last_hourly_data_point = int(self.hourly_data.iloc[int(len(self.hourly_data.index))-1,0])
        self.last_daily_data_point = int(self.daily_data.iloc[int(len(self.daily_data.index))-1,0])

    def process_data(self, data_frame, last_data_point, timing):
        time_since_last_data_point = int(round(time.time()) - last_data_point)
        if time_since_last_data_point >= timing and time_since_last_data_point % timing == 0:
            avgTemp = self.saved_data.iloc[int(len(self.saved_data.index)) - (timing // 5):, 1].mean()
            avgSal = self.saved_data.iloc[int(len(self.saved_data.index))- (timing // 5):, 2].mean()
            avgPh = self.saved_data.iloc[int(len(self.saved_data.index))- (timing // 5):, 3].mean()
            data_frame.loc[round(time.time())] = [round(time.time()), avgTemp, avgSal, avgPh]
            if int(len(data_frame.index)) > 120:
                earliestDataPoint = int(data_frame.iloc[0,0])
                return  data_frame.drop(index=earliestDataPoint, axis=index), int(data_frame.iloc[int(len(data_frame.index))-1,0])
            return data_frame, int(data_frame.iloc[int(len(data_frame.index))-1,0])

    def process_next_data(self, new_data):
        temp, sal, pH = new_data.split(",")
        temp, sal, pH = float(temp), int(sal), float(pH)
        self.saved_data.loc[round(time.time())] = [round(time.time()), temp, sal, pH]

        second_update =  self.process_data(self.second_data, self.last_secondly_data_point, 5)
        if second_update:
            self.second_data, self.last_secondly_data_point = second_update
            second_update = 1
        
        hourly_update = self.process_data(self.hourly_data, self.last_hourly_data_point, 3600)
        if hourly_update:
            self.hourly_data, self.last_hourly_data_point = hourly_update
            hourly_update = 1

        daily_update = self.process_data(self.daily_data, self.last_daily_data_point, 86400)
        if daily_update:
            self.daily_data, self.last_daily_data_point = daily_update
            daily_update = 1

        return second_update, hourly_update, daily_update
        
