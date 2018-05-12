import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from collections import Counter
# 5043 x 28


def get_labels(gross):
    gross_classes = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.4,1.7,2.0,2.4,2.8,3.2,3.6,4.0,4.5,5.0,5.5,6.0,6.5,7.0,float('Inf')]) * 1e8
    
    labels = []
    for i in gross:
        for j in range(len(gross_classes)):
            if gross_classes[j] <= i < gross_classes[j+1]:
                labels.append(j)
    return labels

def remove_column(df, drop_list):
	for col_name in drop_list:
		df.drop(col_name, axis=1, inplace=True)
	return df

def get_genres (dataframe):
	unique_genres = set([])
	for row in dataframe['genres']:
		genres = row.split("|")
		for g in genres:
			unique_genres.add(g)
	unique_genres = sorted(unique_genres)
	return unique_genres

def one_hot_encode_genres (dataframe):
	size =  len(dataframe)
	unique_genres = get_genres (df)
	for genre in unique_genres:
		genre_idx = df[df['genres'].str.contains(genre)].index
		arr = [0] * size
		for i in genre_idx:
			arr[i] = 1
		df[genre] = arr
	return df

def one_hot_encode(dataframe, column):
	size =  len(dataframe)
	unique_genres = np.unique(df[column])
	for genre in unique_genres:
		genre_idx = df[df[column].str.match(genre)].index
		arr = [0] * size
		for i in genre_idx:
			arr[i] = 1
		df[genre] = arr
	return df

def analysis(y_p, y_t):
    diff = y_p - y_t
    
    for i,val in enumerate(diff):
        if val != 0:
            print(y_p[i], y_t[i], val, gross_df[1600+i]) 
            
def wrong_pred_distribution(y_p, y_t):
    diff = y_p - y_t
    c = Counter()
    for i,val in enumerate(diff):
        if val != 0:
            c[y_p[i]] += 1
    return c

def wrong_true_distribution(y_p, y_t):
    diff = y_p - y_t
    c = Counter()
    for i,val in enumerate(diff):
        if val != 0:
            c[y_t[i]] += 1
    return c

            
def get_wrong_index(y_p, y_t):
    diff = y_p - y_t
    index = []
    for i,val in enumerate(diff):
        if val != 0:
            index.append(i)
    return index

df = pd.read_csv("result.csv")
# define this list for the unwanted columns to drop
drop_columns = ["imdbID", "Awards", "BoxOffice", "DVD", "Writer", "Year", "Cumulative Worldwide Gross", "Gross USA"]
df = remove_column(df, drop_columns)

df['movie_title'] = df['movie_title'].str.strip()
df = df.dropna(axis=0, how='any')
df = df.reset_index()

df1 = pd.read_csv("google_index.csv")
sum_index = df1.sum(axis=1)
df1 = pd.concat([df1['title'],sum_index],axis=1, join_axes=[df1.index]).rename(index=str, columns={0: "google_index"})
df = df.merge(right=df1, left_on="movie_title", right_on="title")


gross_df = df['gross']
