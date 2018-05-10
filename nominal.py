
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



def get_labels(gross):
    gross_classes = np.array([0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08, 0.09, float('Inf')]) * 1e8
    
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
		items = str(df[col_name].iloc[i])
		items_arr = items.split(",")
		for item in items_arr:
			item = item.strip()
			if item not in item_map:
				item_map[item] = item_count
				item_count += 1

	Matrix = [[0 for x in range(item_count)] for y in range(movie_size)] 
	for i in range(movie_size):
		items = str(df[col_name].iloc[i])
		items_arr = items.split(",")
		for item in items_arr:
			item = item.strip()
			idx = item_map[item]

			Matrix[i][idx] = 1
	return item_map, np.asarray(Matrix)

def recover_key(dicty,value):
    for a_key in dicty.keys():
        if (dicty[a_key] == value):
            return a_key

df = pd.read_csv('result.csv',index_col=['imdbID'], header=0)
df = df[np.isfinite(df['Opening Weekend USA'])]
df = shuffle(df)

movie_size = (len(df))
test_size = int(movie_size/5)
sample_size = movie_size - test_size

df['BoxOffice'] = df['BoxOffice'].replace( '[\$,)]','', regex=True ).astype(float)
df['Runtime'] = df['Runtime'].replace( 'min','', regex=True ).astype(int)





df['imdbRating'] = df['imdbRating'].round()
labels = get_labels(df['Opening Weekend USA'])


actors_map, actors_Matrix = one_hot_encoding_column('Actors')
genre_map, genre_Matrix = one_hot_encoding_column('Genre')
contry_map, country_Matrix = one_hot_encoding_column('Country')
production_map, production_Matrix = one_hot_encoding_column('Production')
rated_map, rated_Matrix = one_hot_encoding_column('Rated')
year_map, year_Matrix = one_hot_encoding_column('Year')
director_map, director_Matrix = one_hot_encoding_column('Director')

#year_Matrix = df['Year'].as_matrix()
#print(year_Matrix.shape)
#runtime_matrix = df['Runtime'].as_matrix() 
#runtime_matrix = df.loc[:, ['Year', 'Runtime']].as_matrix() 


t_Matrix = np.concatenate((actors_Matrix, \
							production_Matrix,\
							genre_Matrix, \
							country_Matrix, \
							rated_Matrix,\
							year_Matrix
							), axis=1)


f_Matrix = actors_Matrix

print (t_Matrix.shape, t_Matrix.shape )

x_train = t_Matrix[:sample_size]
x_test = t_Matrix[sample_size: ]

y_train = np.array(labels[:sample_size])
y_test = np.array(labels[sample_size: ])

print ("Finished Setting up testing and training set:")
print (x_train.shape, y_train.shape)

#clf_l2_LR = DecisionTreeClassifier()

clf_l2_LR = LogisticRegression(multi_class="multinomial", solver = 'lbfgs')



clf_l2_LR.fit(x_train, y_train)
y_predit = clf_l2_LR.predict(x_test)

"""
importances = clf_l2_LR.feature_importances_
indices = np.argsort(importances)[::-1]
# Print the feature ranking



print("Feature ranking:")

cc = 0
for f in range(t_Matrix.shape[1]):
    print("%d. %s (%f)" % (f + 1, recover_key(director_map, indices[f]), importances[indices[f]]))
    if cc >=20:
    	break
    cc += 1


"""

#for ii in range (len(y_test)):
	#print (y_predit[ii], y_test[ii])


print (np.mean(y_predit == y_test))





