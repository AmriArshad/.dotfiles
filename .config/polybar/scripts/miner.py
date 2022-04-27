#!/bin/python
# -*- coding: utf-8 -*-

import requests

ADDRESS = "0x5493256F6b210a2ABa8289E41FEa50767FC28538"

REQ = requests.get("https://api.ethermine.org/miner/:{}/currentStats".format(ADDRESS))
try:
    # HTTP CODE = OK
    if REQ.status_code == 200:
      data = REQ.json()["data"]
      hashrate = round(int(data["currentHashrate"]) * 10 ** -6, 1)
      print("{} MH/s".format(hashrate))
    else:
        print("Error: BAD HTTP STATUS CODE " + str(REQ.status_code))
except (ValueError, IOError):
    print("Error: Unable print the data")