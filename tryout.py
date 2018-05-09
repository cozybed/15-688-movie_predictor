import numpy
import pandas


df = pandas.read_csv("sample_all.csv")
directors = df['Director'].unique()
print (len(directors))


production = df['Production'].unique()

print (len(production))
