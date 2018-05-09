
import json
import glob
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


df = pd.read_csv('sample_all.csv',index_col=['imdbID'], header=0)
movie_size = (len(df['Actors']))

test_size = int(movie_size/5)
sample_size = movie_size - test_size
print (sample_size)


actors_map = {}
actors_count = 0
for i in range(movie_size):
	actors = df.Actors.iloc[i]
	actors_arr = actors.split(",")
	for actor in actors_arr:
		actor = actor.strip()
		if actor not in actors_map:
			actors_map[actor] = actors_count
			actors_count += 1

Matrix = [[0 for x in range(actors_count)] for y in range(movie_size)] 
for i in range(movie_size):
	actors = df.Actors.iloc[i]
	actors_arr = actors.split(",")
	for actor in actors_arr:
		actor = actor.strip()
		actor_idx = actors_map[actor]

		Matrix[i][actor_idx] = 1

Matrix = np.asarray(Matrix)
sample = Matrix[:sample_size]
test = Matrix[sample_size: ]
print (sample.shape, test.shape)




