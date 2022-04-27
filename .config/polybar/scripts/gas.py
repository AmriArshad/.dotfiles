#!/bin/python
# -*- coding: utf-8 -*-

import requests

REQ = requests.get("https://etherchain.org/api/gasnow")
try:
    # HTTP CODE = OK
    if REQ.status_code == 200:
      data = REQ.json()["data"]
      rapid = round(int(data["rapid"]) * 10 ** -9)
      print("{} GWei".format(rapid))
    else:
        print("Error: BAD HTTP STATUS CODE " + str(REQ.status_code))
except (ValueError, IOError):
    print("Error: Unable print the data")