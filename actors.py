import pandas as pd
import numpy as np

df = pd.read_csv('result.csv',index_col=['imdbID'], header=0)

df = df[np.isfinite(df['Opening Weekend USA'])]
print (len(df))