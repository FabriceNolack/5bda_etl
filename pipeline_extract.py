import luigi
from bs4 import BeautifulSoup as bs
import requests as req, pandas as pd
import os, os.path
from unidecode import unidecode as ud
from datetime import datetime

class Extract(luigi.Task):
    # List of columns of my dataframe.
    COLS = ['name', 'fullname', 'age', 'value', 'wage', 'position', 'origin', 'club', 'duration']

    def output(self):
        os.makedirs('./log', exist_ok=True)
        return luigi.LocalTarget('./log/log_extract.txt')

    def run(self):
        with self.output().open("w") as outfile:
            outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tBEGIN...\n')
            MAX_ITEMS = 60
            MAX_PAGE = 7

            player_list = []
            
            url = "https://sofifa.com/players"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}    
            params = {'type': 'all', 'lg':4, 'showCol[0]': 'ae', 'showCol[1]': 'vl', 'showCol[2]': 'wg'}
            http = req.get(url, headers=headers, params=params)
            outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tThe web site {url} openned with success...\n')
            
            url = http.url

            if http.status_code == req.codes.ok:
                soup = bs(http.content, 'lxml')
                
                outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tContent of the page {url} scrapped BEGIN...\n')

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
                    
                outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tContent of the page {url} scrapped END...\n')
                raw = pd.DataFrame(player_list, columns=self.COLS)
                os.makedirs("data", exist_ok=True)
                raw.to_csv("./data/raw.csv", header=True, index=False)
                outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\traw Data Creata into file ./data/raw.csv...\n')
                # return True
            else:
                # Traitement d'erreur avec try..Except..finally
                print("\n\n\t\tERROR. CANNOT ACCESS THE PAGE...")
                outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tProcess stopped due to an error...\n')
                raw = None
                # return False
            outfile.write(f'{datetime.now().strftime("%d %B %Y %I:%M%p")}\tEND...\n')

