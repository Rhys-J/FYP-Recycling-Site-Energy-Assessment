import datetime
import math
import datetime
import random
from pandas import *
import pandas

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

tonnes = 800 #Per month
weekly_sh = (0.50278  * tonnes / 4.345) * 6
weekly_gl = (0.47241  * tonnes / 4.345) * 6
weekly_tw = (0.28131  * tonnes / 4.345) * 6
sh = [0] * 52560
gl = [0] * 52560
tw = [0] * 52560

real_demand = []
peak_demand = []
energy_demand = []

demand_data = read_csv("Demand_Data/400tonnes_monthly_demand.csv")
demand_times = demand_data['Datetime'].tolist()

wind_data = read_csv("Wind_Data/450kW - Nordex N27 EP.csv")
wind_power = wind_data['electricity']

solar_data = read_csv("Solar_Data/400kW - Solar No tracking.csv")
solar_power = solar_data['electricity']

anytime_power_capacity = 0 #In kW

battery_capacity = 800 # In kWh
battery_c_rate = 0.5
battery_state = "off"
battery_cycles = 0
battery_max_discharge = battery_capacity * battery_c_rate
battery_stored = [battery_capacity/2]

available_power = []
energy_consumed = []
demand_met = []
weekly_demand_failed = []
wind_utilised = []
wind_curtailed = []
solar_utilised = []
solar_curtailed = []
battery_discharged = []
anytime_utilised = []

sh_week_count = 0
gl_week_count = 0
tw_week_count = 0
shflag = 0
glflag = 0
twflag = 0

for i in range(52560):
    timestamp = datetime.datetime(2022, 1, 1, 7)
    timestamp = timestamp + datetime.timedelta(minutes=10*i)
    j = math.floor(i / 6)
    if i % 1008 == 0 and i != 0:
        demand_failed = 0
        if sh_week_count + 6 < weekly_sh:
            demand_failed += (80 + (random.random() * 10)) * (weekly_sh-sh_week_count)
            print("missed sh by " + str(weekly_sh - sh_week_count))
        if gl_week_count + 6 < weekly_gl:
            demand_failed += (150 + (random.random() * 30)) * (weekly_gl-gl_week_count)
            print("missed gl by " + str(weekly_gl - gl_week_count))
        if tw_week_count  + 6 < weekly_tw:
            demand_failed += (100 + (random.random() * 50)) * (weekly_tw-tw_week_count)
            print("missed tw by " + str(weekly_tw - tw_week_count))
        weekly_demand_failed.append(demand_failed)
        sh_week_count = 0
        gl_week_count = 0
        tw_week_count = 0
        shflag = 0
        glflag = 0
        twflag = 0
        if demand_failed > 0:
            print("Weekly demand not met in week " + str(math.floor(i / 1008)))
    
    if 714 - ((i%1008) * (17 / 24))  <= 10 + (weekly_sh - sh_week_count):
        shflag = 1
    if 714 - ((i%1008) * (17 / 24))  <= 10 + (weekly_gl - gl_week_count):
        glflag = 1
    if 714 - ((i%1008) * (17 / 24))  <= 10 + (weekly_tw - tw_week_count):
        twflag = 1
    if shflag == 1 and glflag == 1 and twflag == 1:
        available_power.append(anytime_power_capacity + min(battery_stored[i]*6,battery_max_discharge) + wind_power[j] + solar_power[j])
    elif (shflag == 1 and glflag == 1) or (shflag and glflag) or (glflag and twflag):
        available_power.append(min(400, anytime_power_capacity) + min(battery_stored[i]*6,battery_max_discharge) + wind_power[j] + solar_power[j])
    elif glflag == 1 or twflag == 1 or sh_week_count >= weekly_sh:
        available_power.append(min(300, anytime_power_capacity) + min(battery_stored[i]*6,battery_max_discharge) + wind_power[j] + solar_power[j])
    else:
        available_power.append(min(150, anytime_power_capacity) + min(battery_stored[i]*6,battery_max_discharge) + wind_power[j] + solar_power[j])
    
    temp_available = available_power[i]
    if can_process(timestamp.time()) and available_power[i] >= 520 and sh_week_count < weekly_sh and gl_week_count < weekly_gl and tw_week_count < weekly_tw:
        real_demand.append(290 + (random.random() *  70))
        peak_demand.append(520)
        energy_demand.append(real_demand[i] / 6)
        sh_week_count += 1
        gl_week_count += 1
        tw_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 400 and sh_week_count < weekly_sh and tw_week_count < weekly_tw and glflag != 1:
        real_demand.append(180 + (random.random() * 60))
        peak_demand.append(400)
        energy_demand.append(real_demand[i] / 6)
        sh_week_count += 1
        tw_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 390 and gl_week_count < weekly_gl and tw_week_count < weekly_tw and shflag != 1:
        real_demand.append(210 + (random.random() * 70))
        peak_demand.append(390)
        energy_demand.append(real_demand[i] / 6)
        gl_week_count += 1
        tw_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 360 and sh_week_count < weekly_sh and gl_week_count < weekly_gl and twflag != 1:
        real_demand.append(230 + (random.random() * 40))
        peak_demand.append(360)
        energy_demand.append(real_demand[i] / 6)
        sh_week_count += 1
        gl_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 280 and tw_week_count < weekly_tw and shflag != 1 and glflag != 1:
        real_demand.append(100 + (random.random() * 50))
        peak_demand.append(280)
        energy_demand.append(real_demand[i] / 6)
        tw_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 250 and gl_week_count < weekly_gl and shflag != 1 and twflag != 1:
        real_demand.append(150 + (random.random() * 30))
        peak_demand.append(250)
        energy_demand.append(real_demand[i] / 6)
        gl_week_count += 1
    elif can_process(timestamp.time()) and available_power[i] >= 150 and sh_week_count < weekly_sh and glflag != 1 and twflag != 1:
        real_demand.append(80 + (random.random() * 10))
        peak_demand.append(150)
        energy_demand.append(real_demand[i] / 6)
        sh_week_count += 1
    else:
        real_demand.append(0)
        peak_demand.append(0)
        energy_demand.append(0)

    temp_demand = real_demand[i]
    energy_consumed.append(energy_demand[i])
    demand_met.append(real_demand[i])
    #Priority 1: Wind
    wind_used = min(temp_demand, wind_power[j])
    wind_utilised.append(wind_used)
    wind_to_charge_battery = min(wind_power[j] - wind_used, battery_max_discharge, (battery_capacity-battery_stored[i])*6)
    wind_curtailed.append(wind_power[j] - wind_used - wind_to_charge_battery)
    temp_demand = temp_demand - wind_used
    #Priority 2: Solar
    solar_used = min(temp_demand, solar_power[j])
    solar_utilised.append(solar_used)
    solar_to_charge_battery = min(solar_power[j] - solar_used, battery_max_discharge - wind_to_charge_battery, (battery_capacity-battery_stored[i])*6)
    solar_curtailed.append(solar_power[j] - solar_used - solar_to_charge_battery)
    temp_demand = temp_demand - solar_used
    #Priority 3: Battery and Anytime Power
    if temp_demand > 0:
        if battery_state == "off":
            battery_cycles += 1
        battery_state = "on"
        battery_used = min(temp_demand, battery_max_discharge, battery_stored[i]*6)
        battery_discharged.append(battery_used)
        battery_stored.append(battery_stored[i] - (battery_used/6))
        temp_demand = temp_demand - battery_used
        anytime_utilised.append(temp_demand)
    else:
        battery_state = "off"
        battery_charged = min(battery_max_discharge, wind_to_charge_battery + solar_to_charge_battery, (battery_capacity-battery_stored[i])*6)
        battery_discharged.append(0)
        battery_stored.append(battery_stored[i] + (battery_charged/6))
        anytime_utilised.append(0)

battery_stored.pop()
# print(len(available_power))
# print(len(energy_consumed))
# print(len(demand_met))
# print(len(demand_failed))
# print(len(wind_utilised))
# print(len(wind_curtailed))
# print(len(solar_utilised))
# print(len(solar_curtailed))
# print(len(battery_discharged))
# print(len(anytime_utilised))
# print(len(battery_stored))

print(sum(battery_discharged))
print(sum(solar_curtailed))
print(sum(wind_utilised))
print(max(anytime_utilised))
print(sum(anytime_utilised)/6)
print(sum(demand_met) / 6)

print()
print(battery_cycles)

print(sum(weekly_demand_failed) / 6)

dict = {'datetime': demand_times, 'real demand (kW)': real_demand, 'peak demand (kW)': peak_demand, 'available power (kW)': available_power, 'energy consumed (kWh)': energy_consumed, 'demand met (kW)': demand_met, 'demand failed (kW)': demand_failed, 'wind utilised (kW)': wind_utilised, 'wind curtailed (kW)': wind_curtailed, 'solar utilised (kW)': solar_utilised, 'solar curtailed (kW)': solar_curtailed, 'battery discharged (kW)': battery_discharged, 'battery stored (kWh)': battery_stored, 'anytime utilised (kW)': anytime_utilised}

df = pandas.DataFrame(dict)
df.to_csv('Simulation_Results/Flexi_Demand_800_tonnes/Flexi no anytime v2.csv')