import pandas as pd
import sys

files = ["date0-500and1500-2000", "date500-1000", "date1000-1500", "date2000-2500", "date2500-"]

days = 7


d = {"title":[]}
for i in range(days):
    d['date_index'+str(i)] = []

def get_date_index(line):
    return line.split(',')[:2]


for file in files:
    f = open(file, "r")
    data = f.readlines()
    f.close()
    
    index_t = 0   
    for i,line in enumerate(data):
        line = line.strip()
        if (len(line) >= 5 and line[-5:] == "False") or (len(line)>=4 and line[-4:] == "True"):
            if index_t < days:
                date, index = get_date_index(line)
                d['date_index'+str(index_t)].append(index)
                index_t += 1
        else:
            if ',isPartial' in line or len(line) == 0:
                pass
            elif "\"\"" == line:
                d["title"].pop(-1)
            else:
                if index_t != days and i != 0 and index_t != 0:
                    d["title"].pop(-1)
                    for j in range(index_t):
                        d['date_index'+str(j)].pop(-1)
                    print(file, name, index_t)
                name = line
                d['title'].append(name)
                index_t = 0
    
    for i in d.keys():
        if i != 'title' and len(d[i]) != len(d['title']):
            for i in d.keys():
                print(len(d[i]), i)
            sys.exit(0)
            
df = pd.DataFrame(data=d)
csv_1 = df.to_csv("google_index.csv")
