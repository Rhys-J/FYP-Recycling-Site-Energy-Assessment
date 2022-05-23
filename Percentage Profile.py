import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

#THIS SCRIPT TO TO EXTRACT THE POWER COMSUMPTION FOR EACH OPERATING SCENARIO

#---------------------------------GRANULATING-----------------------------------------------------------

startdate = datetime.datetime(2021, 12, 1) #Set start date, fist date included in analysis
enddate = datetime.datetime(2022, 1, 1) #Set end date, first date exluded in analysis
days_difference =  (enddate - startdate).days
Demand_readings = [0] * math.floor((enddate - startdate).total_seconds() / 600)
SH_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)
GL_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)
TW_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)
SH_TW_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)
SH_GL_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)
GL_TW_on = [0] * math.floor((enddate - startdate).total_seconds() / 600)


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
                Demand_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) / 1000
                if float(AvgCurrent) > 150:
                    GL_on[index] = 1
            last_index = index
            
#---------------------------------SHREDDING-----------------------------------------------------------

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
                    Demand_readings[index] += (float(AvgCurrent) + 80) * 400 * math.sqrt(3) / 1000
                    if GL_on[index] == 1:
                        SH_GL_on[index] = 1
                        GL_on[index] = 0
                    else:
                        SH_on[index] = 1
                else:
                    Demand_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) / 1000
            last_index = index

#---------------------------------TYREWIRE-----------------------------------------------------------

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
                Demand_readings[index] += float(AvgCurrent) * 400 * math.sqrt(3) / 1000
                if float(AvgCurrent) > 20:                    
                    if SH_on[index] == 1:
                        SH_TW_on[index] = 1
                        SH_on[index] = 0
                    elif GL_on[index] == 1:
                        GL_TW_on[index] = 1
                        GL_on[index] = 0
                    else:
                        TW_on[index] = 1
            last_index = index
            
demand0 = 0
demand0To50 = 0
demand50To100 = 0
demand100To150 = 0
demand150To200 = 0
demand200To250 = 0
demand250To300 = 0
demand300To350 = 0
demand350To400 = 0
demand400To450 = 0
demand450To500 = 0
fallthrough = 0

sh_count = 0
gl_count = 0
tw_count = 0
sh_gl_count = 0
sh_tw_count = 0
gl_tw_count = 0
none_count = 0

for i in range(len(Demand_readings)):
    if Demand_readings[i] > 450:
        demand450To500 += 1
    elif Demand_readings[i] > 400:
        demand400To450 += 1
    elif Demand_readings[i] > 350:
        demand350To400 += 1
    elif Demand_readings[i] > 300:
        demand300To350 += 1
    elif Demand_readings[i] > 250:
        demand250To300 += 1
    elif Demand_readings[i] > 200:
        demand200To250 += 1
    elif Demand_readings[i] > 150:
        demand150To200 += 1
    elif Demand_readings[i] > 100:
        demand100To150 += 1
    elif Demand_readings[i] > 50:
        demand50To100 += 1
    elif Demand_readings[i] > 0:
        demand0To50 += 1
    elif Demand_readings[i] == 0:
        demand0 += 1
    else:
        fallthrough += 1

    if SH_on[i] == 1:
        sh_count += 1
    elif GL_on[i] == 1:
        gl_count += 1
    elif TW_on[i] == 1:
        tw_count += 1
    elif SH_TW_on[i] == 1:
        sh_tw_count += 1
    elif GL_TW_on[i] == 1:
        gl_tw_count += 1
    elif SH_GL_on[i] == 1:
        sh_gl_count += 1
    else:
        none_count += 1


print(len(Demand_readings))


print(demand0)
print(demand0To50)
print(demand50To100)
print(demand100To150)
print(demand150To200)
print(demand200To250)
print(demand250To300)
print(demand300To350)
print(demand350To400)
print(demand400To450)
print(demand450To500)
print(fallthrough)

print()

print(none_count)
print(sh_count)
print(gl_count)
print(tw_count)
print(sh_gl_count)
print(sh_tw_count)
print(gl_tw_count)



