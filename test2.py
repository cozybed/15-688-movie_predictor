import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
# 想砍人系列
# 5043 x 28


def get_labels(gross):
    gross_classes = np.array([0,0.2,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.4,1.7,2.0,2.4,2.8,3.2,3.6,4.0,4.5,5.0,5.5,6.0,6.5,7.0,float('Inf')]) * 1e8
    
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



df = pandas.read_csv("movie_metadata.csv")
# define this list for the unwanted columns to drop
drop_columns = ["movie_imdb_link", "plot_keywords", "movie_title", "language"]
df = remove_column(df, drop_columns)

df = df.dropna(axis=0, how='any')
df = df.reset_index()

df = one_hot_encode_genres(df)
csv_1 = df.to_csv("movie_genre.csv") #export

print (df[:5])

y = get_labels(df['gross'])
df = one_hot_encode(df, 'content_rating')
df = one_hot_encode(df, 'country')
df = remove_column(df, ['color','genres','gross', 'content_rating', 'country','actor_1_name','actor_2_name','actor_3_name','director_name'])


X = df.as_matrix()
y = np.array(y)

clf = LogisticRegression()
clf.fit(X[:3500,:], y[:3500])
y_p = clf.predict(X[3500:,:])
print("Validation accuracy:", np.mean(y_p==y[3500:]))