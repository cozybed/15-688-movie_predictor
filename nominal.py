
import json
import glob
import sklearn
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression

def get_labels(gross):
    gross_classes = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.4,1.7,2.0,2.4,2.8,3.2,3.6,4.0,4.5,5.0,5.5,6.0,6.5,7.0,float('Inf')]) * 1e8
    
    labels = []
    for i in gross:
        for j in range(len(gross_classes)):
            if gross_classes[j] <= i < gross_classes[j+1]:
                labels.append(j)
    return labels

def one_hot_encoding_column(col_name):
	item_map = {}
	item_count = 0
	for i in range(movie_size):
		items = df[col_name].iloc[i]
		items_arr = items.split(",")
		for item in items_arr:
			item = item.strip()
			if item not in item_map:
				item_map[item] = item_count
				item_count += 1

	Matrix = [[0 for x in range(item_count)] for y in range(movie_size)] 
	for i in range(movie_size):
		items = df[col_name].iloc[i]
		items_arr = items.split(",")
		for item in items_arr:
			item = item.strip()
			idx = item_map[item]

			Matrix[i][idx] = 1
	return item_map, np.asarray(Matrix)



df = pd.read_csv('result.csv',index_col=['imdbID'], header=0)
df = df[np.isfinite(df['Opening Weekend USA'])]
df = shuffle(df)

movie_size = (len(df))
test_size = int(movie_size/5)
sample_size = movie_size - test_size

df['BoxOffice'] = df['BoxOffice'].replace( '[\$,)]','', regex=True ).astype(float)

df['imdbRating'] = df['imdbRating'].round()
labels = get_labels(df['Opening Weekend USA'])


actors_map, Matrix = one_hot_encoding_column('Actors')

x_train = Matrix[:sample_size]
x_test = Matrix[sample_size: ]

y_train = np.array(labels[:sample_size])
y_test = np.array(labels[sample_size: ])

print ("Finished Setting up testing and training set:")
print (x_train.shape, y_train.shape)

clf_l2_LR = LogisticRegression(penalty='l2', tol=0.01)
clf_l2_LR.fit(x_train, y_train)
y_predit = clf_l2_LR.predict(x_test)

#acc = np.mean(y_predit == y_test)

y_predit = clf_l2_LR.predict(x_test)

print (clf_l2_LR.predict)





