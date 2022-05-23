import datetime
import csv
from random import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

#THIS SCRIPT TO TO EXTRACT THE POWER COMSUMPTION FOR EACH OPERATING SCENARIO

#---------------------------------GRANULATING-----------------------------------------------------------
#Date taken for profile is 20/10/21 Night Shift
startdate = datetime.datetime(2021, 10, 20, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 21, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_GL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_GL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_GL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_GL_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Min_GL_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_GL_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index
            
x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_GL_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_GL_readings, label = "Max I")
plt.plot(x, Min_GL_readings, label = "Min I")
plt.plot(x, Avg_GL_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of Granulation Line")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()

#---------------------------------SHREDDING-----------------------------------------------------------

startdate = datetime.datetime(2021, 9, 30, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 1, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_SH_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_SH_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_SH_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index: 
                if float(AvgCurrent) > 20:
                    Max_SH_readings[index] += (float(MaxCurrent) + 80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_SH_readings[index] += (float(MinCurrent) + 80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_SH_readings[index] += (float(AvgCurrent) + 80) * 400 * math.sqrt(3) * 0.8 / 1000
                else:
                    Max_SH_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_SH_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_SH_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_SH_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_SH_readings, label = "Max I")
plt.plot(x, Min_SH_readings, label = "Min I")
plt.plot(x, Avg_SH_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of Shredder Line")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()


#---------------------------------TYREWIRE-----------------------------------------------------------

startdate = datetime.datetime(2021, 11, 21, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 11, 22, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_TW_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_TW_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_TW_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_TW_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Min_TW_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_TW_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_TW_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                if Max_TW_readings[index] > 300:
                    Max_TW_readings[index] = 300
                Min_TW_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_TW_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index
            
x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_TW_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_TW_readings, label = "Max I")
plt.plot(x, Min_TW_readings, label = "Min I")
plt.plot(x, Avg_TW_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of TyreWire Line")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()



#---------------------------------SH + GL-----------------------------------------------------------

startdate = datetime.datetime(2021, 9, 30, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 1, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_SG_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_SG_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_SG_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                if float(AvgCurrent) > 20:
                    Max_SG_readings[index] += (float(MaxCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_SG_readings[index] += (float(MinCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_SG_readings[index] += (float(AvgCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                else:
                    Max_SG_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_SG_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_SG_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

startdate = datetime.datetime(2021, 10, 20, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 21, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days


with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_SG_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                #if Max_SG_readings[index] > 300:
                #    Max_SG_readings[index] = 300
                Min_SG_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_SG_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index
            
x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_SG_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_SG_readings, label = "Max I")
plt.plot(x, Min_SG_readings, label = "Min I")
plt.plot(x, Avg_SG_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of Shredding & Granulating")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()


#---------------------------------SH + TW-----------------------------------------------------------

startdate = datetime.datetime(2021, 9, 30, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 1, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_ST_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_ST_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_ST_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                if float(AvgCurrent) > 20:
                    Max_ST_readings[index] += (float(MaxCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_ST_readings[index] += (float(MinCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_ST_readings[index] += (float(AvgCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                else:
                    Max_ST_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_ST_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_ST_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

startdate = datetime.datetime(2021, 11, 21, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 11, 22, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_ST_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Min_ST_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_ST_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_ST_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                if Max_ST_readings[index] > 400:
                    Max_ST_readings[index] = 400
                Min_ST_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_ST_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index
            
x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_ST_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_ST_readings, label = "Max I")
plt.plot(x, Min_ST_readings, label = "Min I")
plt.plot(x, Avg_ST_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of Shredding & Tyrewire")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()

#---------------------------------GL + TW-----------------------------------------------------------

startdate = datetime.datetime(2021, 11, 21, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 11, 22, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_GT_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_GT_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_GT_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_GT_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Min_GT_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_GT_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

startdate = datetime.datetime(2021, 10, 20, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 21, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_GT_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                if Max_GT_readings[index] > 380:
                    Max_GT_readings[index] = 350 + (random()*40)
                Min_GT_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_GT_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index
            
x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_GT_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_GT_readings, label = "Max I")
plt.plot(x, Min_GT_readings, label = "Min I")
plt.plot(x, Avg_GT_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Operating Profile of Granulating & Tyrewire")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()

#---------------------------------FULL LINES-----------------------------------------------------------

startdate = datetime.datetime(2021, 11, 21, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 11, 22, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/TW_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    Max_ALL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)#List to store Ah readings
    Min_ALL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    Avg_ALL_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_ALL_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Min_ALL_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_ALL_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

startdate = datetime.datetime(2021, 10, 20, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 21, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/GL_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                Max_ALL_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                if Max_ALL_readings[index] > 380:
                    Max_ALL_readings[index] = 350 + (random()*40)
                Min_ALL_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                Avg_ALL_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

startdate = datetime.datetime(2021, 9, 30, 19) #Set start date, fist date included in analysis
enddate = datetime.datetime(2021, 10, 1, 7) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days

with open("Sensor_Data/SH_Sensor_Data.csv") as csv_file: #Open the csv file specified
    csv_reader = csv.reader(csv_file, delimiter=',') #Get data from csv into python variable
    next(csv_reader, None) #Skip over the headers in the csv file
    last_index = -1
    for row in csv_reader:
        date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
        if date > startdate and date < enddate:
            AhData = row[5].split(",")[0].split(" ")[1]
            AvgCurrent = row[5].split(",")[1].split(" ")[3]
            MaxCurrent = row[5].split(",")[2].split(" ")[3]
            MinCurrent = row[5].split(",")[3].split(" ")[3]
            index = math.floor((date - startdate).total_seconds() / 600)
            if index != last_index:
                if float(AvgCurrent) > 20:
                    Max_ALL_readings[index] += (float(MaxCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_ALL_readings[index] += (float(MinCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_ALL_readings[index] += (float(AvgCurrent)+80) * 400 * math.sqrt(3) * 0.8 / 1000
                else:
                    Max_ALL_readings[index] += float(MaxCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Min_ALL_readings[index] += float(MinCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
                    Avg_ALL_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) * 0.8 / 1000
            last_index = index

x = [startdate + datetime.timedelta(seconds = i*600) for i in range(len(Max_ALL_readings))]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.plot(x, Max_ALL_readings, label = "Max I")
plt.plot(x, Min_ALL_readings, label = "Min I")
plt.plot(x, Avg_ALL_readings, label = "Avg I")
plt.gcf().autofmt_xdate()
plt.legend()
plt.title("Estimated Operating Profile of Full Processing (All Lines)")
plt.xlabel("Time of Day")
plt.ylabel("kW")
plt.show()
