import datetime
import csv
import math
import random
from pandas import *
import pandas

demand_data = read_csv("Demand_Data/800tonnes_monthly_demand.csv")
real_demand = demand_data['Real Power (kW)'].tolist()
peak_demand = demand_data['Peak requirements (kW)'].tolist()
energy_demand = demand_data['energy consumed (kWh)'].tolist()
demand_times = demand_data['Datetime'].tolist()

wind_data = read_csv("Wind_Data/750kW - Nordex N27 EP.csv")
wind_power = wind_data['electricity']

solar_data = read_csv("Solar_Data/500kW - Solar No tracking.csv")
solar_power = solar_data['electricity']

anytime_power_capacity = 600 #In kW

battery_capacity = 0 # In kWh
battery_c_rate = 0.5
battery_state = "off"
battery_cycles = 0
battery_max_discharge = battery_capacity * battery_c_rate
battery_stored = [battery_capacity/2]

available_power = []
energy_consumed = []
demand_met = []
demand_failed = []
wind_utilised = []
wind_curtailed = []
solar_utilised = []
solar_curtailed = []
battery_discharged = []
anytime_utilised = []


for i in range(len(real_demand)):
    j = math.floor(i / 6)
    available_power.append(anytime_power_capacity + min(battery_stored[i]*6,battery_max_discharge) + wind_power[j] + solar_power[j])
    temp_available = available_power[i]
    temp_demand = real_demand[i]
    if available_power[i] < peak_demand[i]:
        #Can not process full amount
        energy_consumed.append(0)
        demand_met.append(0)
        demand_failed.append(real_demand[i])
        wind_utilised.append(0)
        wind_curtailed.append(wind_power[j])
        solar_utilised.append(0)
        solar_curtailed.append(solar_power[j])
        anytime_utilised.append(0)
        battery_discharged.append(0)
        battery_stored.append(battery_stored[i])
        print('Demand not met at ' + str(demand_times[i]))
    else:
        #Can process full amount
        energy_consumed.append(energy_demand[i])
        demand_met.append(real_demand[i])
        demand_failed.append(0)
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
print(sum(demand_failed) / 6)

print()
print(battery_cycles)

dict = {'datetime': demand_times, 'real demand (kW)': real_demand, 'peak demand (kW)': peak_demand, 'available power (kW)': available_power, 'energy consumed (kWh)': energy_consumed, 'demand met (kW)': demand_met, 'demand failed (kW)': demand_failed, 'wind utilised (kW)': wind_utilised, 'wind curtailed (kW)': wind_curtailed, 'solar utilised (kW)': solar_utilised, 'solar curtailed (kW)': solar_curtailed, 'battery discharged (kW)': battery_discharged, 'battery stored (kWh)': battery_stored, 'anytime utilised (kW)': anytime_utilised}

df = pandas.DataFrame(dict)
df.to_csv('Simulation_Results/Static_Demand_800_tonnes/500k solar 750k wind.csv')