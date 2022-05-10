#!/bin/python
# -*- coding: utf-8 -*-

import requests
from datetime import datetime

CITY = "Auckland"
COUNTRY = "NZ"
SCHOOL = 3
URL = "https://api.aladhan.com/v1/timingsByCity?city={}&country={}&method={}".format(CITY, COUNTRY, SCHOOL)

def tdelta(time1, time2):
  # calculate difference
  tdelta = str(datetime.strptime(time2,'%H:%M') - datetime.strptime(time1,'%H:%M')).split(":")
  hours = int(tdelta[0].split(",")[-1])
  minutes = tdelta[1]

  return hours, minutes

REQ = requests.get(URL)
try:
    # HTTP CODE = OK
    if REQ.status_code == 200:
      timings = REQ.json()["data"]["timings"]
      # remove extra timings
      del timings['Imsak']
      # del timings['Sunrise']
      del timings['Sunset']
      del timings['Midnight']
      
      current = datetime.now().time().strftime("%H:%M")

      for time in timings.items():
        # format time
        formatted_time = datetime.strptime(time[1], "%H:%M").time().strftime("%H:%M") 
        # check for next timings
        if current < formatted_time:
          hours, minutes = tdelta(current, formatted_time)
          print("{} in {}:{}".format(time[0], hours, minutes))
          break
      if current >= timings['Isha']:
        # edge case for time between isha and midnight
        hours, minutes = tdelta(current, timings['Fajr'])
        print("{} in {}:{}".format("Fajr", hours, minutes))
    else:
        print("Error: " + str(REQ.status_code))
except (ValueError, IOError):
    print("Error: Unable to print data")