from calendar import week
import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

startdate = datetime.datetime(2021, 5, 1) #Set start date, fist date included in analysis
enddate = datetime.datetime(2022, 3, 1) #Set end date, first date exluded in analysis

days_diff = (enddate - startdate).days

Demand = [0] * math.floor(days_diff)
print(len(Demand))

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = float(row[4])
            index = math.floor((date - startdate).days)
            Demand[index] += AhData * 400 * math.sqrt(3) * 0.8 / 1000

with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = float(row[4])
            index = math.floor((date - startdate).days)
            Demand[index] += (AhData * 2.1) * 400 * math.sqrt(3) * 0.8 / 1000
        
with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = float(row[4])
            index = math.floor((date - startdate).days)
            Demand[index] += AhData * 400 * math.sqrt(3) * 0.8 / 1000

i = 0
moving_average = []
window_size = 10
while i < len(Demand) - window_size + 1:
    this_window = Demand[i:i+window_size]
    window_average = sum(this_window) / window_size
    moving_average.append(window_average)
    i += 1

print(sum(Demand))

x = [startdate + datetime.timedelta(days = i) for i in  range(len(moving_average))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
plt.plot(x, moving_average)
plt.gcf().autofmt_xdate()
plt.title("Daily moving average of Demand with 10 day window size")
plt.xlabel("Date")
plt.ylabel("Energy kWh")
plt.show()