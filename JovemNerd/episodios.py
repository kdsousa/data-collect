# %%
import requests
import datetime
import json 
import pandas as pd

# %%
# ?per+page=1000&page=1

def get_content(**kwargs):
    url = 'https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/'
    resp = requests.get(url, params=kwargs)
    return resp

def save_data(data, format='json'):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

    if format == 'jason':
        with open('data/episodios/jason/{now}.json', 'w') as open_file:
            json.dump(data, open_file)

    if format == 'parquet':
        df = pd.DataFrame(data)
        df.to_parquet('data/episodios/parquet/{now}.parquet', index=False)

## %%
resp = get_content(per_page=1000, page=1)
resp.json()

# %%
