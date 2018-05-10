import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('result.csv',index_col=['imdbID'], header=0)
Openings = df[np.isfinite(df['Opening Weekend USA'])]

#n, bins, patches = plt.hist(openings, bins=50)
#plt.show()

x = [1,2]
y = [1,2]
plt.plot(x,y)
plt.show()