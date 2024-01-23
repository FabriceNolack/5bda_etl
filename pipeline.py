'''
We are looking to build an ETL to get the Price (Value and Wage) af all players in Pro League (Belgium Championship).
1. We will collect data from sofifa.com
2. We will transform those data as well as we can
3. upload them into RDB (MySQL)
'''

from bs4 import BeautifulSoup as bs
import requests as req, pandas as pd
import os, os.path
from unidecode import unidecode as ud
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# List of columns of my dataframe.
COLS = ['name', 'fullname', 'age', 'value', 'wage', 'position', 'origin', 'club', 'duration']

# function that scrap sofifa.com
def extract_etl():
    MAX_ITEMS = 60
    MAX_PAGE = 7

    player_list = []
    
    url = "https://sofifa.com/players"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}    
    params = {'type': 'all', 'lg':4, 'showCol[0]': 'ae', 'showCol[1]': 'vl', 'showCol[2]': 'wg'}
    http = req.get(url, headers=headers, params=params)
    
    url = http.url

    if http.status_code == req.codes.ok:
        soup = bs(http.content, 'lxml')

        for i in range(MAX_PAGE+1) : # => range(8) => 0.1.2..7
            offset = MAX_ITEMS * i
            tr_list = soup.find('article').find('tbody').find_all('tr')
            for tr in tr_list:
                td_list = tr.find_all('td')
                full_name = td_list[1].a['data-tippy-content']
                name = td_list[1].a.string
                age = td_list[2].string
                origin = td_list[1].div.img['title']
                position = td_list[1].div.span.string
                value = td_list[4].string
                wage = td_list[5].string
                club = td_list[3].a.string
                duration = td_list[3].div.string

                # The Player of the line
                player = [ud(name), ud(full_name), ud(age), value, wage, ud(position), ud(origin), ud(club), duration]

                # We append the player to tle player_list
                player_list.append(player)

            # go to next page.
            params = {'offset': offset} 
            http = req.get(url, headers=headers, params=params)
        raw = pd.DataFrame(player_list, columns=COLS)
        os.makedirs("data", exist_ok=True)
        raw.to_csv("./data/raw.csv", header=True, index=False)
        return True
    else:
        # Traitement d'erreur avec try..Except..finally
        print("\n\n\t\tERROR. CANNOT ACCESS THE PAGE...")
        raw = None
        return False
    

# Traitement.

# COLS = ['name', 'fullname', 'age', 'value', 'wage', 'position', 'origin', 'club', 'duration']
# 1. Format des str.
def transform_df():
    # Remove '€'
    # Remove 'K' or 'M'
    # convert to int
    # Do * 1000 for K and * 1000000 for M
    # TODO define.
    # resume the transformation into a function to respect the ETL process steps.
    df = pd.read_csv("./data/raw.csv", index_col=None)
    df['value'] = df.value.str.replace('€', '')
    df.loc[df['value'].str.contains('K'), 'value'] = df['value'].str.replace('K', '')
    df.loc[df['value'].str.contains('M'), 'value'] = df['value'].str.replace('M', '').astype(float) * 1000
    df.value = df.value.astype(float) * 1000
    df.value = df.value.astype(int)


    df['wage'] = df.wage.str.replace('€', '')
    df.loc[df['wage'].str.contains('K'), 'wage'] = df.wage.str.replace('K', '')
    df.loc[df['wage'].str.contains('M'), 'wage'] = df.wage.str.replace('M', '').astype(float) * 1000
    df.wage = df.wage.astype(float) * 1000
    df.wage = df.wage.astype(int)

    df['contract_start'] = df.duration.str.replace('\n', '').str.split(' ').str[0]
    df['contract_end'] = df.duration.str.replace('\n', '').str.split(' ').str[-1]
    
    df.drop("duration", axis=1, inplace=True)
    df.rename(columns={'value': 'price'}, inplace=True)

    df.contract_end.fillna(-1, inplace=True)  
    df.contract_start.fillna(-1, inplace=True)
    df.contract_start = df.contract_start.astype(int)
    df.contract_end = df.contract_end.astype(int)


    print(df.head(5))
    df.to_csv('./data/transformed.csv', header=True, index=False)

def publish():
    dbname = os.getenv('DB_NAME')
    srv = os.getenv('SERVER_NAME')
    username = os.getenv('SRV_USERNAME')
    password = os.getenv('SRV_PASSWORD')
    host = os.getenv('SERVER_HOST')
    port = os.getenv('SERVER_PORT')
    connector = os.getenv("SVR_CONNECTOR")
    
    url = f'{srv}+{connector}://{username}:{password}@{host}:{port}/{dbname}'
    db = create_engine(url, echo=True)

    conn = db.connect()
    df = pd.read_csv('./data/transformed.csv', index_col=None)

    # TODO: Rmove this after.
    df.rename(columns={'value': 'price'}, inplace=True)

    df.contract_end.fillna(-1, inplace=True)  
    df.contract_start.fillna(-1, inplace=True)
    df.contract_start = df.contract_start.astype(int)
    df.contract_end = df.contract_end.astype(int)

    # TODO: Remove all the line bewteen the 2 TODO.

    row_no = df.to_sql('players', conn, if_exists='replace', index=False)
    print(f"Yous just insert {row_no} lines to your SQL DB")

# extract_etl()
