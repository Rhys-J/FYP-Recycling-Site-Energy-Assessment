import datetime
import csv
import math

startdate = datetime.datetime(2021, 5, 1) #Set start date, fist date included in analysis
enddate = datetime.datetime(2022, 1, 1) #Set end date, first date exluded in analysis

print(startdate)
print(enddate)

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    GL_aHcount = 0
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            GL_aHcount += float(row[4])

print("GL Ah usage: ")
print(GL_aHcount)
print("GL kVAh usage: ")
print(GL_aHcount * 400 * math.sqrt(3) / 1000)
print("GL KWh usage: ")
print(GL_aHcount * 400 * math.sqrt(3) * 0.8 / 1000)


with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    SH_aHcount = 0
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            SH_aHcount += (float(row[4])*2.1)

print("SH Ah usage: ")
print(SH_aHcount)
print("SH kVAh usage: ")
print(SH_aHcount * 400 * math.sqrt(3) / 1000)
print("SH KWh usage: ")
print(SH_aHcount * 400 * math.sqrt(3) * 0.8 / 1000)

with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    TW_aHcount = 0
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            TW_aHcount += float(row[4])

print("TW Ah usage: ")
print(TW_aHcount)
print("TW kVAh usage: ")
print(TW_aHcount * 400 * math.sqrt(3) / 1000)
print("TW kWh usage: ")
print(TW_aHcount * 400 * math.sqrt(3) * 0.8 / 1000)


print()
print("Total Ah usage: ")
print(TW_aHcount + SH_aHcount + GL_aHcount)
print("Total kVAh usage: ")
print((TW_aHcount * 400 * math.sqrt(3) / 1000) + (SH_aHcount * 400 * math.sqrt(3) / 1000) + (GL_aHcount * 400 * math.sqrt(3) / 1000))
print("Total kWh usage: ")
print((TW_aHcount * 400 * math.sqrt(3) * 0.8 / 1000) + (SH_aHcount * 400 * math.sqrt(3) * 0.8 / 1000) + (GL_aHcount * 400 * math.sqrt(3) * 0.8 / 1000))
