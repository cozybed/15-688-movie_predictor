import numpy
import pandas

# 想砍人系列
# 5043 x 28

df = pandas.read_csv("movie_metadata.csv")
df = df.dropna(axis=0, how='any')
df = df.reset_index()

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


df = one_hot_encode_genres(df)
print (df[:5])
