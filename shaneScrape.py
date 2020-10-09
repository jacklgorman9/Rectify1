# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:41:06 2020

@author: jackl
"""
def getShane():
    from time import sleep, strftime
    from random import randint
    import pandas as pd
    import numpy as np
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import re
    from webdriver_manager.chrome import ChromeDriverManager
    
    chromedriver_path = 'C:/Users/jackl/Scrap/chromedriver.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.get('https://fs.blog/knowledge-project/')
    pageScrape = driver.page_source
    soup = BeautifulSoup(pageScrape, 'html.parser')
    knowledge_episodes = soup.find('div',class_='column75 column-center')
    episodes = knowledge_episodes.find_all('p')
    description = []
    episode_name = []
    id_num = []
    link = []
    for ep in episodes:
        if 'Episode' in ep.get_text():
            desc = ep.get_text()
            num = ep.find('strong').get_text()
            num = num.split(':')[0]
            id_num.append(num)
            episode_name.append(ep.find('a').get_text())
            link.append(ep.find('a')['href'])
            #taking out the details that are already supplied (only description left)
            desc = re.sub(num,'',desc)
            desc = re.sub(ep.find('a').get_text(),'',desc)
            desc = re.sub('—','',desc)
            desc = re.sub(':','',desc)
            desc = desc.strip()
            description.append(desc)
    df_shane = pd.DataFrame({'ID':id_num,
                             'Episode' : episode_name,
                             'Description': description,
                             'Link': link})
    df_shane['Podcast Name']  = 'The Knowledge Project'
    df_shane['Image'] = "static/Shane.jpg"
    return df_shane