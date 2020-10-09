from time import sleep, strftime
from random import randint
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#%%
chromedriver_path = 'C:/Users/jackl/Scrap/chromedriver.exe'
driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get('https://tim.blog/podcast/')
#%%
pageScrape = driver.page_source
soup = BeautifulSoup(pageScrape, 'html.parser')
tim_episodes = soup.find('div',{"id": 'tim-ferriss-podcast-list'})
episodes = tim_episodes.find_all('a')
ep = []
link = []
for tim in episodes:
    ep.append(tim.get_text())
    link.append(tim['href'])
#%%
df = pd.DataFrame([ep,link])
df.to_csv('TimFerris.csv')
#%%   
chromedriver_path = 'C:/Users/jackl/Scrap/chromedriver.exe'
driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get('https://tim.blog/podcast/')
desc = [] 
for page in link:
    driver.get(page)
    sleep(3)
    pageScrape = driver.page_source
    soup = BeautifulSoup(pageScrape, 'html.parser')
    description = soup.find_all('p')
    tag = []
    for word in description:
        tag.append(word.get_text())
    desc.append(tag)
#%%
def getDescription(row):
    # if type(row) == 'list':
    row = pd.DataFrame(row)
    row = row[row[0].str.contains('@')]
    if row.empty:
        return 'No description for the person found'
    else:
        return row.iloc[0,0]
    # elif type(row) == 'pandas.core.series.Series':
    #     row = row[row[0].str.contains('@')]
    #     return row[0]
    # else:
    #     return 'No description'
        
desc2 = desc
desc3 = desc2
i = 0
while i < len(desc2):
    desc2[i] = getDescription(desc2[i])
    i += 1
    