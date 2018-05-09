import numpy
import pandas
import twitter

# 想砍人系列
# 5043 x 28

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



df = pandas.read_csv("movie_metadata.csv")
# define this list for the unwanted columns to drop
drop_columns = ["movie_imdb_link", "plot_keywords", ]
df = remove_column(df, drop_columns)

df = df.dropna(axis=0, how='any')
df = df.reset_index()

df = one_hot_encode_genres(df)
csv_1 = df.to_csv("movie_genre.csv")
print (df[:5])
