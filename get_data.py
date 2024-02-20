# data analysis for GDP fred data

from fredapi import Fred
import pandas as pd
import os 
from datetime import datetime

# get key
API_KEY = os.environ['FRED_API_KEY']
# initialize fred api
fred = Fred(api_key=API_KEY)

def get_data(data_id, name):
    # get data
    data = fred.get_series(data_id).to_dict()
    # write to file
    with open(f'data/{name}.csv', 'w') as f:
        f.write('date,value\n')
        for k, v in data.items():
            date_val = str(k).split(" ")[0]
            # skip data earlier than 1959
            if datetime.strptime(date_val, '%Y-%m-%d') < datetime(1959, 1, 1):
                continue
            f.write(f'{date_val},{v}\n')

# get_data('GDPC1', 'gdp_data')
# get_data('GDPDEF', 'price_deflator')
# get_data('UNRATE', 'headline_unemployment')
# get_data('U6RATE', 'u6_unemployment')