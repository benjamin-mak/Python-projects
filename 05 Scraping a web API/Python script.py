#Scraping all historical Singapore relative humidity readings between a specified time period 
#URL:https://data.gov.sg/dataset/realtime-weather-readings?resource_id=59eb2883-2ceb-4d16-85f0-7e3a3176ef46

import requests
import json
import pandas as pd
import numpy as np
import datetime as date
import os


#User to input start and end dates required
while True:
    start_date = input("Enter a start date in the format 'yyyy-mm-dd':")
    if len(start_date) != 10:
        continue
    elif int(start_date[:4]) in range(2024) and int(start_date[5:7]) in range(13) and int(start_date[8:]) in range(32):
        break
    else:
        continue

while True:
    end_date = input("Enter a end date in the format 'yyyy-mm-dd':")
    if len(end_date) != 10:
        continue
    elif not(int(end_date[:4]) in range(2024) and int(end_date[5:7]) in range(13) and int(end_date[8:]) in range(32)):
        continue
    elif date.datetime.strptime(start_date, '%Y-%m-%d').date() <= date.datetime.strptime(end_date, '%Y-%m-%d').date():
        break
    else:
        continue

#Create a list of dates from the input time period
datelist = pd.period_range(start=start_date, end=end_date)

#dictionary for readings
readings = {"timestamp": [], "station_id": [], "value": []}
#dictionary for stations
stations = {"id": [], "device_id": [], "name": [], "latitude": [], "longitude": []}

for date in datelist:
    #pull data from api for specified time period
    response_API = requests.get("https://api.data.gov.sg/v1/environment/relative-humidity?date=" + str(date))
    data = response_API.text
    parse_json = json.loads(data)

    #Add readings to dictionary
    for i in parse_json["items"]:
        for j in i["readings"]:
            readings["timestamp"].append(i["timestamp"])
            readings["station_id"].append(j["station_id"])
            readings["value"].append(j["value"])

    #Add stations to dictionary
    for x in parse_json["metadata"]["stations"]:
        stations["id"].append(x["id"])
        stations["device_id"].append(x["device_id"])
        stations["name"].append(x["name"])
        stations["latitude"].append(x["location"]["latitude"])
        stations["longitude"].append(x["location"]["longitude"])

#create a dataframe from the dictionary
readings_df = pd.DataFrame(readings)
readings_df.index = np.arange(1, len(readings_df) + 1)
#create a dataframe from the dictionary
stations_df = pd.DataFrame(stations)
stations_df.index = np.arange(1, len(stations_df) + 1)

#export to csv file
readings_df.to_csv(os.getcwd() + '\\readings_df' + f'_{start_date}.csv', header=True)
stations_df.to_csv(os.getcwd() + '\\stations_df' + f'_{start_date}.csv', header=True)
print(f"Export completed! Files are in the path '{os.getcwd()}'.")