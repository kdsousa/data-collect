# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,pt-PT;q=0.8,pt;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # 'cookie': '_gid=GA1.2.1152888861.1751901149; __gads=ID=32ab6504c6996bb5:T=1751901149:RT=1751901149:S=ALNI_Ma4IOv9BMDOt-xTZp8JMy7T0lEmUw; __gpi=UID=000010d7d643d01e:T=1751901149:RT=1751901149:S=ALNI_MYOlkUYvbtSIaosBubKabjueUTzeg; __eoi=ID=2f6bf2188d3a15ec:T=1751901149:RT=1751901149:S=AA-AfjZMk4pB2yNJjwguBBob8rtM; _ga=GA1.1.1698630467.1751901126; FCNEC=%5B%5B%22AKsRol-XPdwvTGFDNaUtK0UpvCqJ7Mw66kFm9u8wjDALxaPSF7nNB0f179z8dK4tRpQaz2qQKN-yLSJZP_Zi5_bHfv_zSj3UG1OQFSLVE0gXVxwAd-XY2p16ugqXLcvL0sqz7gvIQNUPw2IyUFRAtk4V_cCCDv9VUA%3D%3D%22%5D%5D; _ga_DJLCSW50SC=GS2.1.s1751901126$o1$g1$t1751901317$j25$l0$h0; _ga_D6NF5QC4QT=GS2.1.s1751901149$o1$g1$t1751901317$j25$l0$h0',
    }

def get_content(url):

    response = requests.get(url, headers=headers)
    return response


def get_basic_infos(soup):

    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(':')
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data


def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
                .find('h4')
                .find_next()
                .find_all('li'))

    aparicoes = [i.text for i in lis]
    return aparicoes


def get_personagem_infos(url):
    
    response = get_content(url)
    if response.status_code != 200:
        print('Não foi possível obter os dados')
        return {}

    else:
        soup = BeautifulSoup(response.text)
        data = get_basic_infos(soup)
        data['aparicoes'] = get_aparicoes(soup)
        return data


def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    response = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(response.text)
    ancoras = (soup_personagens.find('div', class_='td-page-content')
                            .find_all('a'))

    links = [i['href'] for i in ancoras]
    return links

# %%

links= get_links()
data = []

for i in tqdm(links):
    d = get_personagem_infos(i)
    d['link'] = i 
    nome = i.strip('/').split('/')[-1].replace('-', ' ').title()
    d['Nome'] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df

# %%
df.to_parquet('dados_re.parquet', index=False)

# %%
df_nwe = pd.read_parquet('dados_re.parquet')
df_nwe
