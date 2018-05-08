import numpy as np
import pandas
import matplotlib.pyplot as plt
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


'''
unique_genres = get_genres (df)


for genre in unique_genres:
	genre_idx = df[df['genres'].str.contains(genre)].index
	
'''


def get_labels(gross):
    gross_classes = np.array([0,0.2,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.4,1.7,2.0,2.4,2.8,3.2,3.6,4.0,4.5,5.0,5.5,6.0,6.5,7.0,float('Inf')]) * 1e8
    
    labels = []
    for i in gross:
        for j in range(len(gross_classes)):
            if gross_classes[j] <= i < gross_classes[j+1]:
                labels.append(j)
    return labels


print(get_labels(df['gross'])[:20])
