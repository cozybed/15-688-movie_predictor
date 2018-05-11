import json
import glob
import sklearn
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import normalize
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

def get_labels(gross):
    gross_classes = np.array([0,0.5,1, 2,3,4,5, float('Inf')]) * 1e8
    
    labels = []
    for i in gross:
        for j in range(len(gross_classes)):
            if gross_classes[j] <= i < gross_classes[j+1]:
                labels.append(j)
    return labels

def one_hot_encoding_column(col_name, delimiter=','):
	item_map = {}
	item_count = 0
	for i in range(movie_size):
		items = str(df[col_name].iloc[i])
		items_arr = items.split(delimiter)
		for item in items_arr:
			item = item.strip()
			if item not in item_map:
				item_map[item] = item_count
				item_count += 1

	Matrix = [[0 for x in range(item_count)] for y in range(movie_size)] 
	for i in range(movie_size):
		items = str(df[col_name].iloc[i])
		items_arr = items.split(delimiter)
		for item in items_arr:
			item = item.strip()
			idx = item_map[item]

			Matrix[i][idx] = 1
	return item_map, np.asarray(Matrix)


df = pd.read_csv('result.csv',index_col=['imdbID'], header=0)
df = df.loc[:,['imdbRating','imdbVotes', 'critic number', 'user review number', 'Actors','Country', 
               'Genre', 'Production', 'Rated', 'Year', 'Runtime', 'BoxOffice']]
df = df.dropna(axis=0, how='any')
df = df.reset_index()

df['BoxOffice'] = df['BoxOffice'].replace( '[\$,)]','', regex=True ).astype(float)
df['Runtime'] = df['Runtime'].replace( 'min','', regex=True ).astype(int)
df['imdbVotes'] = df['imdbVotes'].replace( ',','', regex=True ).astype(int)
df['imdbRating'] = df['imdbRating']
df = shuffle(df)

movie_size = (len(df))
test_size = int(movie_size/5)
sample_size = movie_size - test_size



labels = get_labels(df['BoxOffice'])


actors_map, actors_Matrix = one_hot_encoding_column('Actors')
genre_map, genre_Matrix = one_hot_encoding_column('Genre')
contry_map, country_Matrix = one_hot_encoding_column('Country')
production_map, production_Matrix = one_hot_encoding_column('Production')
rated_map, rated_Matrix = one_hot_encoding_column('Rated')
runtime_matrix = normalize(df.loc[:, ['Year', 'Runtime']].as_matrix(), axis=0) 
other_features = df.loc[:, ['imdbRating','imdbVotes', 'critic number', 'user review number']].as_matrix()


t_Matrix = np.concatenate((actors_Matrix, 
							genre_Matrix, 
							country_Matrix, 
                                production_Matrix,
							rated_Matrix,
                                runtime_matrix,
                                other_features
							), axis=1)

print (t_Matrix.shape, t_Matrix.shape )

x_train = t_Matrix[:sample_size]
x_test = t_Matrix[sample_size: ]

y_train = np.array(labels[:sample_size])
y_test = np.array(labels[sample_size: ])

print ("Finished Setting up testing and training set:")
print (x_train.shape)

#clf_l2_LR = DecisionTreeClassifier()

clf_l2_LR = LogisticRegression(multi_class="multinomial", solver = 'lbfgs')
clf_l2_LR.fit(x_train, y_train)
y_predit = clf_l2_LR.predict(x_test)
print("Validation accuracy:", np.mean(y_predit==y_test))

######
######
'''
clf =  MLPClassifier(alpha=0.3,activation='logistic')
clf.fit(x_train, y_train)
y_p = clf.predict(x_test)
print("Validation accuracy:", np.mean(y_p==y_test))
'''
'''
clf = SVC()
clf.fit(x_train, y_train)
y_p = clf.predict(x_test)
print("Validation accuracy:", np.mean(y_p==y_test))
'''

'''
#################
clf = KNeighborsClassifier(7)
clf.fit(x_train, y_train)
y_p = clf.predict(x_test)
print("Validation accuracy:", np.mean(y_p==y_test))
'''

#################
clf_tree = DecisionTreeClassifier(max_depth=5)
clf_tree.fit(x_train, y_train)
y_p = clf_tree.predict(x_test)
print("Validation accuracy:", np.mean(y_p==y_test))

#for ii in range (len(y_test)):
#	print (y_predit[ii], y_test[ii])


#print (np.mean(y_predit == y_test))





