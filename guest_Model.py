# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:16:14 2020

@author: jackl
"""
def podcastModelGuest(picker):
    import pandas as pd
    from sklearn.neighbors import NearestNeighbors
    from  sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    import re
    from Podcast_Clean import cleanData
    
    #getting the clean data from the previous file
    df_clean = cleanData()
    
    #final clena for Joe Rogan data       
    def cleanDescriptionFinal(row):
        #removes the episode number
        row = re.sub('To download: Right-Click and save target as.\n\n\n\nSHARE\n\n','',row)
        row = re.sub('\n','',row)
        row = re.sub('\t','',row)
        row = re.sub('  ','',row)
        row = re.sub(u'\xa0', u' ',row)
        row = row.strip()#getting rid of extra spaces
        #attempts to get rid of repeating names at the beginning of JRE episode descriptions.
        if len(row.split(' ')) > 2:
            row = row.split(' ',1)[1]
            row = row.split(' ',1)[1]
        return row
    #adds in the selected material as its own row to fit to the data
    new_row = pd.DataFrame().reindex_like(df_clean)
    new_row['Description'][0] = picker
    new_row = new_row.dropna(subset = ['Description']) #drops all the blank rows from df
    new_row['Episode'] = picker #adds the picker just in case we need to 
    df_clean = pd.concat([df_clean,new_row],ignore_index = True) #combining the new row to the dataframe
    #modeling
    tfid = TfidfVectorizer(stop_words='english',lowercase = True) #usetfid to call out words and names that are prominent in a bio
    X_tfid = tfid.fit_transform(df_clean['Description'])
    #calling nearest neighbors to idenitfy thte closet features for each episode
    nn = NearestNeighbors(n_neighbors = 50).fit(X_tfid)    
    distances, indices = nn.kneighbors(X_tfid,return_distance = True)
    #index for calling the picker
    index1 = np.where(df_clean['Description'] == picker)[0][0]
    rec1 = df_clean.iloc[indices[index1],:].reset_index(drop = True)
    #due to the nature of the the token I actually use the guest for the closet choice instead for guests
    index = np.where(df_clean['Description'] == rec1['Description'][2])[0][0]
    #removes the inputted variable from the dataframe
    rec = df_clean.iloc[indices[index],:].reset_index(drop = True)
    rec = rec.dropna(subset = ['ID']).reset_index(drop = True)
    #removes duplicates and names with strong associations from the list from JRE and Aubrey Marcus from Joe Rogan form showing up because his episodes are annoying
    selected = rec['Episode'][0]
    selected_pod = rec['Podcast Name'][0]
    split_select = selected.split(' ')
    #TFS has a longer tilte where as the others are just the name of the person making it easier to duplicate
    def removeNames(row,split_select,selected):
        duplicate = 0
        if any(ext in row for ext in split_select):
            duplicate = 1
        if selected in row:
            duplicate = 0
        if 'Aubrey Marcus' in row:
            duplicate = 1
        return duplicate
    rec['Duplicate'] = rec['Episode'].apply(lambda x : removeNames(x,split_select,selected))
    if selected_pod == 'The Tim Ferris Show':
        rec.loc[(rec['Podcast Name'] == 'The Tim Ferris Show'),'Duplicate'] = 0
    rec = rec[rec['Duplicate'] == 0]
    
    #final_reccomendations= pd.merge(rec[['ID','Title']],df_clean[['ID','Full Description','Episode Link','Reference 1','Reference 1 Link','Reference 2','Referene 2 Link', 'You Tube Link']],on = ['ID'], how = 'left')
    final_reccomendations = rec[['ID','Episode','Description','Link','Podcast Name','Image']]
    mask = final_reccomendations['Podcast Name'] == 'The Joe Rogan Experience'
    final_reccomendations.loc[mask,'Description'] = final_reccomendations['Description'].apply(lambda x : cleanDescriptionFinal(x))
    #final_reccomendations['Link'] = final_reccomendations['Link'].apply(lambda x: re.sub('http://','',x))

    return (picker, final_reccomendations)
