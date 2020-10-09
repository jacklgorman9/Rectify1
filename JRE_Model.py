def JRE_Model(picker):    
    import pandas as pd
    from sklearn.preprocessing import normalize
    from sklearn. preprocessing import MinMaxScaler
    from sklearn.neighbors import NearestNeighbors
    from  sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    import re
    def cleanDescriptionFinal(row):
        clean_row = []
        filtered_row = []
        #removes the episode number
        row = re.sub('To download: Right-Click and save target as.\n\n\n\nSHARE\n\n','',row)
        row = re.sub('\n','',row)
        row = re.sub('\t','',row)
        row = re.sub('  ','',row)
        row = re.sub(u'\xa0', u' ',row)
        split =row.split('.')
        row = re.sub(split[0], '', row)
        row = re.sub(split[-1],'', row)
        row = re.sub(split[1],'', row)
        row = re.sub(split[2],'', row)
        return row
    
    df_clean = pd.read_csv('Cleaned Data.csv')
    scaler = MinMaxScaler()
    #the early episodes did not have youtube videos filled them with zeros a way to show they are also earleir
    df_clean['Views'] = df_clean['Views'].fillna(0)
    df_clean['Views'] = scaler.fit_transform(df_clean[['Views']])
    new_row = pd.DataFrame().reindex_like(df_clean)
    new_row['Tokenized'][0] = picker
    new_row = new_row.dropna(subset = ['Tokenized'])
    new_row['Title'] = picker
    new_row['Description'] = df_clean['Full Description'][0]
    new_row['Full Description'] = df_clean['Full Description'][0]
    df_clean = pd.concat([df_clean,new_row],ignore_index = True)
    x_unsupervised  = df_clean[['ID','Title','Title_Tokenized','Tokenized']]
      
    x_unsupervised.reset_index()
    tfid = TfidfVectorizer(stop_words='english')
    X_tfid = tfid.fit_transform(x_unsupervised['Tokenized'])
    
    nn = NearestNeighbors(n_neighbors = 50).fit(X_tfid)    
    distances, indices = nn.kneighbors(X_tfid,return_distance = True)
    
    index1 = np.where(x_unsupervised['Tokenized'] == picker)[0][0]
    rec1 = x_unsupervised.iloc[indices[index1],[0,1,2,3]].reset_index(drop = True)
    
    index = np.where(x_unsupervised['Tokenized'] == rec1['Tokenized'][2])[0][0]
    rec = x_unsupervised.iloc[indices[index],[0,1]].reset_index(drop = True)
    rec = rec.dropna(subset = ['ID'])
    
    selected = rec['Title'][0]
    split_select = selected.split(' ')
    def removeNames(row,split_select,selected):
        duplicate = 0
        if any(ext in row for ext in split_select):
            duplicate = 1
        if selected in row:
            duplicate = 0
        if 'Aubrey Marcus' in row:
            duplicate = 1
        return duplicate
    rec['Duplicate'] = rec['Title'].apply(lambda x : removeNames(x,split_select,selected))
    rec = rec[rec['Duplicate'] == 0]
    final_reccomendations= pd.merge(rec[['ID','Title']],df_clean[['ID','Full Description','Episode Link','Reference 1','Reference 1 Link','Reference 2','Referene 2 Link', 'You Tube Link']],on = ['ID'], how = 'left')
    final_reccomendations['Full Description'] = final_reccomendations['Full Description'].apply(lambda x : cleanDescriptionFinal(x))
    return (picker, final_reccomendations)

# if __name__ == '__main__':
#     from pprint import pprint
#     print("Checking to see what empty string predicts")
#     print('input string is ')
#     chat_in = 1400
#     pprint(chat_in)    
#     x_input, probs = JRE_Model(chat_in)
#     print(f'Input values: {x_input}')
#     print('Output probabilities')
#     print(probs)