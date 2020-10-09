# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 23:32:42 2020

@author: jackl
"""
#%%
def cleanData():
    import pandas as pd
    import numpy as np
    import re
    from JRE_clean import JRE_Clean
    
    def timClean():
        df_Tim = pd.read_csv('Tim Data.csv')
        #function that obtains the episode number from the title by looking for the hashtag. 
        #If there is no hastag it returns 0 to show it couldnt be found
        def hashtag(row):
            rows = row.split(' ')
            ep_num = '0'
            for r in rows:
                if '#' in r:
                    ep_num = r
            ep_num = re.sub('\(','',ep_num)
            ep_num = re.sub('\)','',ep_num)
            return ep_num
        df_Tim['ID'] = df_Tim['Episode'].apply(lambda x: hashtag(x))    
        df_Tim = df_Tim.loc[:, ~df_Tim.columns.str.contains('^Unnamed')]#removing unnamed columns
        df_Tim = df_Tim[['ID','Episode','Description','Link']]
        df_Tim['Podcast Name'] = 'The Tim Ferris Show'
        return df_Tim
    #%%
    #Cleans scraped rich roll data
    def richClean():
        df_Rich = pd.read_csv('Rich Roll Data.csv')
        #gets the Episode Number for the ID
        def getEpisode(row):
            rows = row.split('\n')
            row = re.sub('Episode','',rows[0])
            return row
        
        df_Rich['ID'] = df_Rich['Description'].apply(lambda x: getEpisode(x))    
        df_Rich = df_Rich[df_Rich['Episode'] != 'Cant find title']
        df_Rich = df_Rich[df_Rich['Episode'] != 'Roll On:']
        df_Rich = df_Rich[df_Rich['Episode'] != 'THE RICH ROLL PODCAST']
        #cuts off the ads and other non important, non guest parts
        df_Rich['Description'] = df_Rich['Description'].apply(lambda x: (x.partition('on Apple')[0]))
        #some descriptions dont have this feature so we will add in another key phrase
        df_Rich['Description'] = df_Rich['Description'].apply(lambda x: (x.partition('Sign up for Roll')[0]))
        df_Rich['Description'] = df_Rich['Description'].apply(lambda x: (x.partition('iTunes')[0]))
        df_Rich = df_Rich.loc[:, ~df_Rich.columns.str.contains('^Unnamed')]#removing unnamed columns
        #gets the Episode Number for the IDp 
        df_Rich = df_Rich[['ID','Episode','Description','Link']]
        df_Rich['Podcast Name'] = 'The Rich Roll Podcast'
        return df_Rich
    #merging all the data 
    #%%
    def oneMerge():
        df_Rich = richClean()
        df_Tim = timClean()
        df_JRE = JRE_Clean()
        df_clean = pd.concat([df_Rich,df_Tim,df_JRE])
        df_clean = df_clean.reindex()
        return df_clean

