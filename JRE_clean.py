def JRE_Clean(): 
    import pandas as pd
    import numpy as np
    import datetime
    import re 
    import string
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')
    df_main = pd.read_csv('JRE_Main.csv')
    df_youTube = pd.read_csv('JRE_YouTube.csv')
    df_categories = pd.read_csv('JRE_Categories.csv')
    #goign too youtube set
    def findEP(row):
        split = row.split(' ')
        ep_num = []
        for word in split:
            if '#' in word:
                ep_num.append(word)
        ep_num = ep_num[0]
        return int(ep_num[1:].replace('-',''))
    #dropping all now JRE episodes
    df_youTube = df_youTube[df_youTube['Title'].str.startswith('Joe Rogan Experience #')]    
    df_youTube['ID'] = df_youTube['Title'].apply(lambda x : findEP(x))
    #dropping title column and unamed column as they wont be necessary when we merge them
    df_youTube = df_youTube.drop(['Title'], axis=1)
    df_youTube = df_youTube.loc[:, ~df_youTube.columns.str.contains('^Unnamed')]
    
    def getViews(row):
        split = row.split(' ')[0]
        num = 0 
        if 'M' in split:
            num =  float(split[:-1]) * 1000000
        if 'K' in split:
            num = float(split[:-1]) * 1000
        return num
    df_youTube['Views'] = df_youTube['Views'].apply(lambda x : getViews(x))
    df_youTube['You Tube Link'] = df_youTube['You Tube Link'].apply(lambda x: 'https://youtube.com' + x)
    #Cleaning Categories Frame
    #dropping any that do not have an episode number
    df_categories = df_categories[df_categories['Title'].str.contains('#')]
    df_categories['ID'] = df_categories['Title'].apply(lambda x : findEP(x))
    categories = df_categories.groupby('ID')['Category'].unique().reset_index()
    unique = pd.DataFrame(df_categories['Category'].unique(), columns = ['Cat'])
    #removing unnecessary/ categories that dont make sense. Will have to update code if I ever update this
    unique = unique.drop([55,56,61])
    #adding the columns as a list
    columns = ['ID']
    for i in unique['Cat']:
        columns.append(i)
    df_dummies= pd.DataFrame(np.zeros((int(len(categories)),int(len(unique))+1)),columns = columns)
    #df_dummies = pd.merge(df_dummies,categories,on = ['ID'],how = 'inner')
    df_dummies['ID'] =categories['ID']
    #simple function that allows me to correctly identify if the category is in the row for dummy purposes
    def plusOne(row, name):
        how = 0 
        if name in row:
            how = 1
        return how 
    #adding in the category colum to make it easier to pass it into the lambda function
    
    df_dummies['Category'] = categories['Category']
    for c in columns[1:]:
        df_dummies[c] = df_dummies['Category'].apply(lambda x : plusOne(x,c))
    
    #Time for cleaning the third data frame 
    df_main['Episode ID'] = df_main['Episode ID'].apply(lambda x : x[1:])
    #df_main['Episode ID'] = df_main['Episode ID'].filter(regex='\d+')
    df_main =  df_main[~df_main['Episode ID'].str.contains('[A-Za-z]')]
    df_main['Date'] = df_main['Date'].apply(lambda x : datetime.datetime.strptime(x, '%m.%d.%y'))
    #getting rid of fight companions
    df_main = df_main[~df_main['Title'].str.contains('Fight Companion')]
    #getting rid of MMA Episodes
    df_main = df_main[~df_main['Title'].str.contains('MMA Show')]
    df_main = df_main[~df_main['Title'].str.contains('Fight Recap')]
    df_main = df_main[~df_main['Title'].str.contains('Recap')]
    #manually filling in empties. Could apply description function but probably easier just to do this
    df_main.loc[df_main['Title']=='Tony Hawk','Episode ID'] = '1477'
    df_main.loc[df_main['Title']=='Andrew Doyle','Episode ID'] = '1423'
    df_main.loc[df_main['Title']=='Owen Benjamin & Kurt Metzger','Episode ID'] = '1093'
    df_main['Episode ID'] = df_main['Episode ID'].apply(lambda x : int(x))
    #getting rid of uneccessary columns & cleaning column names
    df_main = df_main.loc[:, ~df_main.columns.str.contains('^Unnamed')]
    df_main = df_main.rename(columns = {'Episode ID':'ID'})
    df_main = df_main.drop_duplicates()
    df_main = df_main.drop(['Description'],axis = 1)
    #relinking the old descriptions 
    df_descriptions = pd.read_csv('JRE_Full_Links.csv')
    df_descriptions = df_descriptions[~df_descriptions['Title'].str.contains('Fight Companion')]
    #getting rid of MMA Episodes
    df_descriptions = df_descriptions[~df_descriptions['Title'].str.contains('MMA Show')]
    df_descriptions = df_descriptions[~df_descriptions['Title'].str.contains('Fight Recap')]
    df_description = df_descriptions[~df_descriptions['Title'].str.contains('Recap')]
    df_descriptions.loc[df_descriptions['Title']=='Tony Hawk','Episode ID'] = '1477'
    df_descriptions.loc[df_descriptions['Title']=='Andrew Doyle','Episode ID'] = '1423'
    df_descriptions.loc[df_descriptions['Title']=='Owen Benjamin & Kurt Metzger','Episode ID'] = '1093'
    df_descriptions =  df_descriptions[~df_descriptions['Episode ID'].str.contains('[A-Za-z]')]
    df_descriptions =  df_descriptions[~df_descriptions['Full Description'].str.contains('UFConFOX fight card',na = False)]
    df_descriptions =  df_descriptions[~df_descriptions['Full Description'].str.contains('Joe sits down with Tony Hinchcliffe on a plane to',na = False)]
    df_descriptions['ID'] = df_descriptions['Episode ID'].apply(lambda x : int(x[1:]))
    df_descriptions = df_descriptions[['ID','Full Description']]
    
    
    #merging dataframes
    df_clean = pd.merge(df_main,df_youTube, on =['ID'],how = 'outer')
    df_clean = pd.merge(df_clean,df_dummies, on = ['ID'], how = 'outer')
    df_clean = pd.merge(df_clean,df_descriptions, on = ['ID'], how = 'outer')
    
    #Going to add the title to tokenize hoepfully then there may be a similarity in words??
    
    df_clean['Full Description'] = df_clean['Full Description'].fillna(df_clean['Title'])
    df_clean = df_clean[df_clean['Title'].notna()]
    df_clean = df_clean.drop_duplicates(subset='ID', keep='first')
    #meant to scrub description of key words as well clean overall tidiness before vectorization
    def cleanDescription(row):
        clean_row = []
        filtered_row = []
        #removes the episode number
        row = re.sub('To download: Right-Click and save target as.\n\n\n\nSHARE\n\n','',row)
        row = re.sub('\n','',row)
        row = re.sub('\t','',row)
        row = re.sub('  ','',row)
        row = re.sub(u'\xa0', u' ',row)
        row = re.sub('\.(?!\d)', '',row)
        row = re.sub(r'[^A-Za-z ]+', '', row)
        row = re.sub('available on Apple Podcasts', '' , row)
        return row
    # def cleanDescriptionFinal(row):
    #     clean_row = []
    #     filtered_row = []
    #     #removes the episode number
    #     row = re.sub('To download: Right-Click and save target as.\n\n\n\nSHARE\n\n','',row)
    #     row = re.sub('\n','',row)
    #     row = re.sub('\t','',row)
    #     row = re.sub('  ','',row)
    #     row = re.sub(u'\xa0', u' ',row)
    #     split =row.split('.')
    #     row = re.sub(split[0], '', row)
    #     row = re.sub(split[-1],'', row)
    #     row = re.sub(split[1],'', row)
    #     row = re.sub(split[2],'', row)
    #     return row
    
    df_clean['Tokenized'] = df_clean['Full Description'].apply(lambda x : cleanDescription(x))
    df_clean['Title_Tokenized'] = df_clean['Title'].apply(lambda x : cleanDescription(x))
    #Saving a copy just in case
    df_clean.to_csv('Cleaned Data.csv')
    df_JRE = df_clean[['ID','Title','Tokenized','Episode Link']]
    df_JRE['Podcast Name'] = 'The Joe Rogan Experience'
    df_JRE = df_JRE.rename(columns={'Title': 'Episode', 'Tokenized': 'Description','Episode Link':'Link'})
    df_JRE['Description'] = df_JRE['Description'].apply(lambda x: re.sub('JRE','',x))
    df_JRE['Image'] = "static/JRE.jpg"
    return df_JRE
