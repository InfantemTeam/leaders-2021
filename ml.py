import numpy as np
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from pandas.core.frame import DataFrame
from pymystem3 import Mystem
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
nltk.download("stopwords")
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

def create_soup(x):
    """ Merge all data about book x """
    return ' '.join([x.title, x.aut.replace(" ",""), x.serial, x.lan, x.rubrics, x.annotation])

def preprocess_text(text):
    """ Remove punctuation characters, stop-words from string """
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
                and token != " " \
                and token.strip() not in punctuation ]
    text = " ".join(tokens)
    return text

def postprocess_text(text):
    """ Remove special symbols, numbers and broken tokens """
    tmp = re.sub(r'\s+', ' ', re.sub(r'[\d_]', '', re.sub(r'[^\w\s]', '', text)))
    return ' '.join(set(tmp.split(' ')))

def load_data_from_files():
    """ Load dataset, preparing and transforming in pd.DataFrames """
    # READ FILES INTO VARIABLES WITH SAME NAME AS FILES
    cat1 = pd.read_csv('dataset/cat_1.csv',sep=';',encoding = "windows-1251",low_memory=False)
    cat2 = pd.read_csv('dataset/cat_2.csv',sep=';',encoding = "windows-1251",low_memory=False)
    cat3 = pd.read_csv('dataset/cat_3.csv',sep=';',encoding = "windows-1251",low_memory=False)
    dataset_knigi_1 = pd.read_csv('dataset/dataset_knigi_1.csv',sep=';',encoding = "windows-1251",low_memory=False)
    readers = pd.read_csv('dataset/readers.csv',sep=';',encoding = "windows-1251",low_memory=False)
    annotation = pd.read_csv('dataset/annotation.csv',sep=';',encoding = "windows-1251",low_memory=False)
    # CONCAT _1, _2, _3... FILES IN ONE
    cat = pd.concat([cat1,cat2,cat3],ignore_index=True)
    # CLEAR DATA FROM GARBAGE COLUMNS
    readers = readers.loc[:,~readers.columns.str.match("Unnamed")]
    # REPAIR BAD FILES WITHOUT COLUMN LABELS
    readers.loc[-1] = readers.columns
    readers.index = readers.index+1
    readers = readers.sort_index()
    readers.columns = ["abis_id","dateOfBirth","Address"]
    annotation.loc[-1] = annotation.columns
    annotation.index = annotation.index+1
    annotation = annotation.sort_index()
    annotation.columns = ["id","annotation"]

    tmp = dataset_knigi_1['source_url']
    bookId = []
    for i in tmp:
        bookId.append(int(i.split('/')[-2]))
    bookId = pd.DataFrame(bookId,columns=['book_id'])
    book_circ = dataset_knigi_1.merge(bookId, left_index=True, right_index=True)
    book_circ = book_circ[['book_id','user_id']]

    book_data=pd.DataFrame(book_circ['book_id'].unique(),columns=['book_id'])
    book_data=book_data.merge(cat[['recId','title','aut','serial','lan','rubrics','ager']],left_on='book_id', right_on='recId',how='left')
    book_data=book_data.merge(annotation,left_on='book_id', right_on='id',how='left')
    book_data=book_data.drop(columns=['recId','id'])
    book_data=book_data.drop_duplicates(subset='book_id')
    book_data=book_data.reset_index()
    # CLEAN
    book_data['ager'] = book_data['ager'].str.replace('+','',regex=False)
    book_data['ager'] = pd.to_numeric(book_data['ager'], errors='coerce').fillna(0).astype(np.int64)
    book_data = book_data.fillna('')

    book_data['soup']=book_data.apply(create_soup,axis=1)
    book_data['soup']=book_data['soup'].apply(preprocess_text)
    book_data['soup']=book_data['soup'].apply(postprocess_text)
    
    return (book_data,book_circ,readers)

book_data, book_circ, book_readers = load_data_from_files()

def model_fit(book_data):
    """ Create similarity matrix """
    count = TfidfVectorizer()
    count_matrix = count.fit_transform(book_data['soup'])
    product = linear_kernel(count_matrix, count_matrix)
    return product

books_similarity = model_fit(book_data)

def model_find_similar(book_id):
    """ Find similar books for given book ID """
    max_pred = 11
    similarity = list(enumerate(books_similarity[book_id]))
    similarity = sorted(similarity, key=lambda x: x[1], reverse=True)
    similarity = similarity[1:max_pred]
    movie_indices = [i[0] for i in similarity]
    return movie_indices

def model_recommend(user_id, rec_num=5):
    """ Make raw prediction for user """
    if user_id:
        # If user exists, then give recommendations given on his library history
        book_indicies = book_circ[book_circ.user_id==user_id].book_id
        if(len(book_indicies)>=rec_num):
            ids = list(zip(book_indicies[-rec_num:],[1]*rec_num))
        else:
            ids = []
            j=1
            while len(ids)<rec_num:
                for i in book_indicies:
                    ids.append((i,j))
                j+=1
        predictions = []
        for i,j in ids:
            predictions.append(model_find_similar(book_data[book_data.book_id==i].index.values.tolist()[0])[j])
        predicted_ids = []
        for i in predictions:
            predicted_ids.append(book_data[book_data.index==i].book_id.item())
    else:
        # Recommended book_id's for new user
        # Give most tranding books
        book_id, counts = np.unique(book_circ.book_id, return_counts=True)
        bookFreq = pd.DataFrame(zip(book_id, counts), columns=['id','count'])
        predicted_ids = bookFreq.sort_values(by='count', ascending=[False])[:rec_num].id
    return predicted_ids

def generate_result_csv():
    """ Generate out.csv file according to result_task3.csv template """
    users = book_circ.user_id.unique()
    output = pd.DataFrame(columns=['user_id','book_id_1','book_id_2','book_id_3','book_id_4','book_id_5'])
    for i in range(len(users)):
        res=model_recommend(users[i])
        output.loc[i] = [users[i]]+res
    print(output)
    output.to_csv('out.csv',sep=';',encoding='utf-8',index=False)

def transform2JSON(recommended_ids,user_id):
    """ Transform raw predictions to JSON format """
    rec_objcts=[{"id":i, \
                "title":book_data.loc[book_data['book_id']==i,'title'].item(), \
                "author":book_data.loc[book_data['book_id']==i,'aut'].item()} for i in recommended_ids ]
    historical_ids = list(book_circ[book_circ.user_id==user_id].book_id)
    hist_objcts=[{"id":i, \
                "title":book_data.loc[book_data['book_id']==i,'title'].item(), \
                "author":book_data.loc[book_data['book_id']==i,'aut'].item()} for i in historical_ids ]
    return {"recommendations":rec_objcts,"history":hist_objcts}

def model_predict(user_id, rec_num=5):
    """ Make prediction and prepare them for API """
    id_list = model_recommend(user_id,rec_num=rec_num)
    return transform2JSON(id_list,user_id)
