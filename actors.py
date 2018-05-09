import pandas


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

actors = set([])

df = pandas.read_csv("movie_metadata.csv")
df = df.dropna(axis=0, how='any')


actors_1 = set(df['actor_1_name'])
#actors_2 = set(df['actor_2_name'])
#actors_3 = set(df['actor_3_name'])

print (len(actors_1))
#print (len(actors_2))
#print (len(actors_3))


actors = sorted(actors_1)
str = ""
for a in actors:
	if a.find(" ") < 0:
		print (a)
	if not isEnglish(a):
		print (a)
	else:
		str+= a + "\n"

with open('workfile.csv', 'w') as f:
	f.write(str)
	f.close()