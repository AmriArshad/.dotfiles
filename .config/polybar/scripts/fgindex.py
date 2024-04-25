#!/usr/bin/env python3

import requests

# API endpoint for the fear and greed index
url = "https://api.alternative.me/fng/"

try:
    # Send a GET request to the API
    response = requests.get(url)
    data = response.json()

    # Extract the fear and greed index value
    index_class = data['data'][0]['value_classification']
    index_value = data['data'][0]['value']

    print(f"{index_class}: {index_value}")
except Exception as e:
    print("Error:", e)
