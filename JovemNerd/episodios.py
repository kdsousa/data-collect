# %%
import requests
import datetime
import json 
import pandas as pd
import os
import time

# %%
# ?per+page=1000&page=1

def get_content(**kwargs):
    url = 'https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/'
    resp = requests.get(url, params=kwargs)
    return resp

def save_data(data, format='json'):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

    if format == 'json':
        with open(f'data/episodios/json/{now}.json', 'w') as open_file:
            json.dump(data, open_file)

    if format == 'parquet':
        df = pd.DataFrame(data)
        df.to_parquet(f'data/episodios/parquet/{now}.parquet', index=False)

# %%
page = 1
while True:
    print(page)
    resp = get_content(per_page=1000, page=1)
    if resp.status_code == 200:
        data = resp.json()
        save_data(data)

        if len(data) < 100:
            break

        page += 1
        time.sleep(2)

    else:
        print(resp.status_code)
        print(resp.json())
        time.sleep(60 * 5)

# %%
