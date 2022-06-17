import datetime
import csv
import math
import random

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
-0.50278 hours shredding
-0.47241 hours granulating
-0.28131 hours tyrewire

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
    Peak_values = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    sh = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    gl = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    tw = [0] * math.floor((yearend - yearstart).total_seconds() / 600)

    with open('Demand_Data/' + str(tonnes) + 'tonnes_monthly_demand.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['Datetime', 'SH', 'GL', 'TW', 'Current Draw (A)', 'Real Power (kW)', 'Peak requirements (kW)', 'Apparent Power (kVA)', 'energy consumed (kWh)']
        writer.writerow(header)
        date = yearstart
        weekly_sh = (0.50278  * tonnes / 4.345) * 6
        weekly_gl = (0.47241  * tonnes / 4.345) * 6
        weekly_tw = (0.28131  * tonnes / 4.345) * 6
        week_start = datetime.datetime(2022, 4, 18, 7)
        week_end = datetime.datetime(2022, 4, 25, 7)
        sh_count = 0
        gl_count = 0
        tw_count = 0
        sh_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        gl_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)
        tw_week = [0] * math.floor((week_end - week_start).total_seconds() / 600)

        date = week_start
        loop = 0
        while sh_count < weekly_sh and loop < 3:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                sh_week[index] = 1
                sh_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=24)
            if date >= week_end:
                if loop == 0:
                    date = week_start + datetime.timedelta(hours=24)
                if loop == 1: 
                    date = week_start + datetime.timedelta(hours=12)
                loop += 1
                if loop == 3:
                    print("Max limit of tyre processing exceeded")
                

        date = week_start + datetime.timedelta(hours=12)
        loop = 0
        while gl_count < weekly_gl and loop < 3:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                gl_week[index] = 1
                gl_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=24)
            if date >= week_end:
                if loop == 0:
                    date = week_start
                if loop == 1:
                    date = week_start + datetime.timedelta(hours=24)
                loop += 1

        date = week_start + datetime.timedelta(hours=24)
        loop = 0
        while tw_count < weekly_tw and loop < 4:
            index = math.floor((date - week_start).total_seconds() / 600)
            if can_process(date.time()):
                tw_week[index] = 1
                tw_count += 1
            date = date + datetime.timedelta(minutes=10)
            if date.time() == datetime.time(7) or date.time() == datetime.time(19):
                date = date + datetime.timedelta(hours=36)
            if date >= week_end:
                if loop == 0:
                    date = week_start + datetime.timedelta(hours=12)
                if loop == 1:
                    date = week_start 
                if loop == 2: 
                    date = week_start + datetime.timedelta(hours=36)
                loop += 1

        date = yearstart + datetime.timedelta(hours=7)
        for i in range(len(Demand_readings)):
            sh[i] = sh_week[i%1008]
            gl[i] = gl_week[i%1008]
            tw[i] = tw_week[i%1008]
            if sh[i] == 1 and gl[i] == 1 and tw[i] == 1:
                Demand_readings[i] = 290 + (random.random() *  70)
                #Demand_readings[i] = random.triangular(290, 360, 325)
                Peak_values[i] = 520
            elif sh[i] == 1 and gl[i] == 1:
                Demand_readings[i] = 230 + (random.random() * 40)
                #Demand_readings[i] = random.triangular(230, 270, 250)
                Peak_values[i] = 360
            elif sh[i] == 1 and tw[i] == 1:
                Demand_readings[i] = 180 + (random.random() * 60)
                #Demand_readings[i] = random.triangular(180, 240, 210)
                Peak_values[i] = 400
            elif gl[i] == 1 and tw[i] == 1:
                Demand_readings[i] = 210 + (random.random() * 70)
                #Demand_readings[i] = random.triangular(210, 280, 245)
                Peak_values[i] = 390
            elif sh[i] == 1:
                Demand_readings[i] = 80 + (random.random() * 10)
                #Demand_readings[i] = random.triangular(80, 90, 85)
                Peak_values[i] = 150
            elif gl[i] == 1:
                Demand_readings[i] = 150 + (random.random() * 30)
                #Demand_readings[i] = random.triangular(150, 180, 165)
                Peak_values[i] = 250
            elif tw[i] == 1:
                Demand_readings[i] = 100 + (random.random() * 50)
                #Demand_readings[i] = random.triangular(100, 150, 125)
                Peak_values[i] = 280

            
            data = [date, sh[i], gl[i], tw[i], Demand_readings[i]*1000/(400*0.8*math.sqrt(3)), Demand_readings[i], Peak_values[i], Demand_readings[i]/0.8, Demand_readings[i]/6]
            writer.writerow(data)
            date = date + datetime.timedelta(minutes=10)


def Demand_2021():

    yearstart = datetime.datetime(2021, 1, 1) 
    yearend = datetime.datetime(2022, 1, 1) 
    Demand_readings = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    Peak_values = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    sh = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    gl = [0] * math.floor((yearend - yearstart).total_seconds() / 600)
    tw = [0] * math.floor((yearend - yearstart).total_seconds() / 600)

    with open('Sensor_Data/GL_Sensor_Data.csv') as GL_file:
        csv_reader = csv.reader(GL_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date = date.replace(second=0)
            if minute == 60:
                date = date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date = date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            Demand_readings[index] += float(row[4])
            if float(row[4]) > 20:
                gl[index] = 1
                Peak_values[index] = 250

    with open('Sensor_Data/SH_Sensor_Data.csv') as SH_file:
        csv_reader = csv.reader(SH_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date = date.replace(second=0)
            if minute == 60:
                date = date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date = date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            if float(row[4]) > 5:
                Demand_readings[index] += (float(row[4]) + 13)
                sh[index] = 1
                if gl[index] == 1:
                    Peak_values[index] = 360
                else:
                    Peak_values[index] = 150
            else:
                Demand_readings[index] += float(row[4])

    with open('Sensor_Data/TW_Sensor_Data.csv') as TW_file:
        csv_reader = csv.reader(TW_file, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            date = datetime.datetime.strptime(row[3], '%d/%m/%Y %H:%M:%S')
            minute = round(date.minute, -1)
            date = date.replace(second=0)
            if minute == 60:
                date = date.replace(minute=0)
                date = date + datetime.timedelta(hours=1)
            else:
                date = date.replace(minute=minute)
            if date.year == 2021:
                index = math.floor((date - yearstart).total_seconds() / 600)
            else:
                index = math.floor((date - yearend).total_seconds() / 600)
            Demand_readings[index] += float(row[4])
            if float(row[4]) > 5:
                tw[index] = 1
                if sh[index] == 1:
                    Peak_values[index] = 400
                elif gl[index] == 1:
                    Peak_values[index] = 390
                else:
                    Peak_values[index] = 280
                    

    with open('Demand_Data/2021_Demand.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['Datetime', 'SH', 'GL', 'TW', 'Current Draw (A)', 'Real Power (kW)', 'Peak requirements (kW)', 'Apparent Power (kVA)', 'energy consumed (kWh)']
        writer.writerow(header)
        date = yearstart
        for i in range(len(Demand_readings)):
            data = [date, sh[i], gl[i], tw[i], Demand_readings[i]*6, Demand_readings[i]*400*6*0.8*math.sqrt(3)/1000, Peak_values[i], Demand_readings[i]*400*6*math.sqrt(3)/1000, Demand_readings[i]*400*0.8*math.sqrt(3)/1000]
            writer.writerow(data)
            date = date + datetime.timedelta(minutes=10)



#Demand_2021()
static_demand(800)