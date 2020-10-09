from time import sleep, strftime
from random import randint
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

chromedriver_path = 'C:/Users/jackl/Scrap/chromedriver.exe'
driver = webdriver.Chrome(ChromeDriverManager().install()) 
website = 'https://www.richroll.com/category/podcast/'
driver.get(website)
#%%
pageScrape = driver.page_source
soup = BeautifulSoup(pageScrape, 'html.parser')
blocks = soup.find('div',class_ = 'clearfix row')
links = blocks.find_all('a')
href = []
for link in links:
    href.append(link['href'])
driver.close()
#%%
chromedriver_path = 'C:/Users/jackl/Scrap/chromedriver.exe'
driver = webdriver.Chrome(ChromeDriverManager().install()) 
ep = []
description = []
for h in href:
    driver.get(h)
    pageScrape = driver.page_source
    try:
        soup = BeautifulSoup(pageScrape, 'html.parser')
        title = soup.find('h1',class_='rrp-hero-head').get_text()
        ep.append(title)
        paragraph = soup.find_all('p')
        string = ''
        for p in paragraph:
            string = string + p
        description.append()
    except('Link does not work for 'h)
    