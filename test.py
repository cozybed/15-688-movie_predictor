import numpy
import pandas

# 想砍人系列
# 5043 x 28

df = pandas.read_csv("movie_metadata.csv")
df = df.dropna(axis=0, how='any')
size =  len(df)

def get_genres (dataframe):
	unique_genres = set([])
	for row in dataframe['genres']:
		genres = row.split("|")
		for g in genres:
			unique_genres.add(g)
	unique_genres = sorted(unique_genres)
	return unique_genres


unique_genres = get_genres (df)


for genre in unique_genres:
	genre_idx = df[df['genres'].str.contains(genre)].index
	
