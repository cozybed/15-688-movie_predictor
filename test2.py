import numpy as np
import pandas
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
            print(y_p[i], y[i], val, gross_df[3500+i]) 
            
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

df = pandas.read_csv("movie_metadata.csv")
# define this list for the unwanted columns to drop
drop_columns = ["movie_imdb_link", "plot_keywords", "movie_title", "language"]
df = remove_column(df, drop_columns)

df = df.dropna(axis=0, how='any')
df = df.reset_index()

gross_df = df['gross']

y = get_labels(df['gross'])

df = one_hot_encode_genres(df)
#csv_1 = df.to_csv("movie_genre.csv") #export
df = one_hot_encode(df, 'content_rating')
df = one_hot_encode(df, 'country')
df = remove_column(df, ['director_facebook_likes', 'actor_3_facebook_likes', 'actor_1_facebook_likes', 'cast_total_facebook_likes',
'facenumber_in_poster', 'actor_2_facebook_likes', 'movie_facebook_likes','aspect_ratio',
        'index', 'color','genres','gross', 'content_rating', 'country','actor_1_name','actor_2_name','actor_3_name','director_name'])


X = df.as_matrix()
y = np.array(y)

#################
clf_lg = LogisticRegression()
clf_lg.fit(X[:3500,:], y[:3500])
y_p = clf_lg.predict(X[3500:,:])
print("Validation accuracy:", np.mean(y_p==y[3500:]))

#analysis(y_p, y[3500:])
print(wrong_pred_distribution(y_p, y[3500:]))
print(wrong_true_distribution(y_p, y[3500:]))


#################
clf = SVC()
clf.fit(X[:3500,:], y[:3500])
y_p = clf.predict(X[3500:,:])
'''
for i, val in enumerate(y_p):
    if val == 0:
        y_p[i] = clf_lg.predict(X[i,:].reshape(1, -1))
'''
print("Validation accuracy:", np.mean(y_p==y[3500:]))

print(wrong_pred_distribution(y_p, y[3500:]))
print(wrong_true_distribution(y_p, y[3500:]))


#################
clf =  MLPClassifier(alpha=0.3,activation='logistic')
clf.fit(X[:3500,:], y[:3500])
y_p = clf.predict(X[3500:,:])
print("Validation accuracy:", np.mean(y_p==y[3500:]))

print(wrong_pred_distribution(y_p, y[3500:]))
print(wrong_true_distribution(y_p, y[3500:]))


#################
clf = KNeighborsClassifier(7)
clf.fit(X[:3500,:], y[:3500])
y_p = clf.predict(X[3500:,:])
print("Validation accuracy:", np.mean(y_p==y[3500:]))

print(wrong_pred_distribution(y_p, y[3500:]))
print(wrong_true_distribution(y_p, y[3500:]))


#################
clf_tree = DecisionTreeClassifier(max_depth=5)
clf_tree.fit(X[:3500,:], y[:3500])
y_p = clf_tree.predict(X[3500:,:])
print("Validation accuracy:", np.mean(y_p==y[3500:]))

print(wrong_pred_distribution(y_p, y[3500:]))
print(wrong_true_distribution(y_p, y[3500:]))


for i, val in enumerate(clf_tree.feature_importances_):
    if val != 0:
        print(df.columns[i],'\t', val)
