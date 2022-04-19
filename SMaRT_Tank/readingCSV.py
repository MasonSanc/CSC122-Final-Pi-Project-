import pandas as pd

liveData = pd.read_csv('liveData.csv')
times = liveData['time'].to_numpy()
temps = liveData['temp'].to_numpy()
salinity = liveData['salinity'].to_numpy()
pH = liveData['pH'].to_numpy()

print(times)
print(temps)
print(salinity)
print(pH)
