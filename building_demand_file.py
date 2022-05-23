import datetime
import csv
import math
from random import random

# yearstart = datetime.datetime(2022, 4, 17) 
# print(yearstart.weekday())

"""
(Assuming 8.5 hours of processing per 12h shift)
For 400 tonnes of tyres in a month:
-Shred for 200 hours (23.5 shifts)
-Granulate for 190 hours (22 shifts)
-Tyrewire for 110 hours (13 shifts)

Broken down into a week (assuming 4.375 weeks in a month)
-Shred for 46 hours (5.4 shifts)
-Granulate for 43 hours (5 shifts)
-Tyrewire for 25 hours (3 shifts)

For every tonne of processing in a month:
-0.5 hours shredding
-0.475 hours granulating
-0.275 hours tyrewire

Need to create function that builds up demand and necessary operations
for a given tyre monthly intake
It must attempt to prioritise nightime procesing and spread out the demand
evenly
"""
def can_process(time):
    if datetime.time(7, 30) <= time < datetime.time(10):
        return True
    if datetime.time(10, 30) <= time < datetime.time(13):
        return True
    if datetime.time(14) <= time < datetime.time(16):
        return True
    if datetime.time(16, 30) <= time < datetime.time(18):
        return True
    if datetime.time(19, 30) <= time < datetime.time(22):
        return True
    if datetime.time(22, 30) <= time:
        return True
    if time < datetime.time(1):
        return True
    if datetime.time(2) <= time < datetime.time(4):
        return True
    if datetime.time(4, 30) <= time < datetime.time(6):
        return True
    return False

def static_demand(tonnes):
    yearstart = datetime.datetime(2021, 1, 1) 
    yearend = datetime.datetime(2022, 1, 1) 
    Demand_readings = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    sh = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    gl = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    tw = [0] * math.floor((yearend - yearstart).total_seconds() / 600)

    with open('Demand_Data/' + str(tonnes) + 'tonnes_monthly_demand.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['Datetime', 'SH', 'GL', 'TW', 'Current Draw', 'Real Power', 'Apparent Power', 'kWh used']
        writer.writerow(header)
        date = yearstart
        weekly_sh = (0.5 * tonnes / 4.375) * 6
        weekly_gl = (0.475 * tonnes / 4.375) * 6
        weekly_tw = (0.275 * tonnes / 4.375) * 6
        week_start = datetime.datetime(2022, 4, 18, 7)
        week_end = datetime.datetime(2022, 4, 25, 7)
        sh_count = 0
        gl_count = 0
        tw_count = 0
        Demand_weekly = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        sh_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        gl_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        tw_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        date = week_start
        while sh_count < weekly_sh:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                sh_week[index] = 1
                Demand_weekly[index] += (144 + (random()*20))
                sh_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=24)
            if date >= week_end:
                date = week_start + datetime.timedelta(hours=24)

        date = week_start + datetime.timedelta(hours=12)
        while gl_count < weekly_gl:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                gl_week[index] = 1
                Demand_weekly[index] += (277 + (random()*90))
                gl_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=24)
            if date >= week_end:
                date = week_start

        date = week_start + datetime.timedelta(hours=24)
        while tw_count < weekly_tw:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                tw_week[index] = 1
                if gl_week[index] == 1:
                    Demand_weekly[index] += (100 + random()*30)
                else:
                    Demand_weekly[index] += (207 + (random()*43))
                tw_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=24)
            if date >= week_end:
                date = week_start + datetime.timedelta(hours=12)

        date = yearstart + datetime.timedelta(hours=7)
        for i in range(len(Demand_readings)):
            sh[i] = sh_week[i%1008]
            gl[i] = gl_week[i%1008]
            tw[i] = tw_week[i%1008]
            Demand_readings[i] = Demand_weekly[i%1008]
            data = [date, sh[i], gl[i], tw[i], Demand_readings[i], Demand_readings[i]*400*0.8*math.sqrt(3)/1000, Demand_readings[i]*400*math.sqrt(3)/1000, Demand_readings[i]*400*0.8*math.sqrt(3)/(1000*6)]
            writer.writerow(data)
            date = date + datetime.timedelta(minutes=10)


def Demand_2021():

    yearstart = datetime.datetime(2021, 1, 1) 
    yearend = datetime.datetime(2022, 1, 1) 
    Demand_readings = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    sh = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    gl = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    tw = [0] * math.floor((yearend - yearstart).total_seconds() / 600)


    with open('Sensor_Data/GL_Sensor_Data.csv') as GL_file:
        csv_reader = csv.reader(GL_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date.replace(second=0)
            if minute == 60:
                date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            Demand_readings[index] += float(row[4])
            if float(row[4]) > 5:
                gl[index] = 1

    with open('Sensor_Data/SH_Sensor_Data.csv') as SH_file:
        csv_reader = csv.reader(SH_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date.replace(second=0)
            if minute == 60:
                date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            if float(row[4]) > 5:
                Demand_readings[index] += (float(row[4]) + 13)
                sh[index] = 1
            else:
                Demand_readings[index] += float(row[4])

    with open('Sensor_Data/TW_Sensor_Data.csv') as TW_file:
        csv_reader = csv.reader(TW_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date.replace(second=0)
            if minute == 60:
                date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            Demand_readings[index] += float(row[4])
            if float(row[4]) > 5:
                tw[index] = 1

    with open('Demand_Data/2021_Demand.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['Datetime', 'SH', 'GL', 'TW', 'Current Draw', 'Real Power', 'Apparent Power', 'kWh used']
        writer.writerow(header)
        date = yearstart
        for i in range(len(Demand_readings)):
            data = [date, sh[i], gl[i], tw[i], Demand_readings[i]*6, Demand_readings[i]*400*6*0.8*math.sqrt(3)/1000, Demand_readings[i]*400*6*math.sqrt(3)/1000, Demand_readings[i]*400*0.8*math.sqrt(3)/1000]
            writer.writerow(data)
            date = date + datetime.timedelta(minutes=10)



#Demand_2021()
static_demand(400)