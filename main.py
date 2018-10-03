import numpy as np
import pandas as pd
from pandasql import sqldf
q = lambda q: sqldf(q, globals())
import re

pd.options.display.html.table_schema = True
pd.options.display.max_rows = None

### ETL

df

# Get Datasets
df = pd.read_csv('/Users/peterjmyers/work/Taxi-Trip-Time-Prediction/data/train.csv', sep=",", nrows=500)
# train_df = pd.read_csv('/Users/cheryljose/Documents/Projects/all/train.csv', sep=",", nrows=500)
df.head()
metadata_df = pd.read_csv('/Users/peterjmyers/work/Taxi-Trip-Time-Prediction/data/metaData_taxistandsID_name_GPSlocation.csv', sep=",", nrows=500)
# metadata_df = pd.read_csv('/Users/cheryljose/Documents/Projects/all/metaData_taxistandsID_name_GPSlocation.csv', sep=",", nrows=500)
test_df = pd.read_csv('/Users/peterjmyers/work/Taxi-Trip-Time-Prediction/data/test.csv', sep=",", nrows=500)
#test_df = pd.read_csv('/Users/cheryljose/Documents/Projects/all/test.csv', sep=",", nrows=500)

# Get the time taken in total
df['polyline_length'] = df['POLYLINE'].apply(lambda x: len(x.split("],[")))
df['time_taken'] = df['polyline_length'].apply(lambda x: (x - 1) * 15)
df.head()

# edit 41st line of metadata
metadata_df['Latitude'][40] = 41.163066654
metadata_df['Longitude'][40] = -8.67598304213
metadata_df.iloc[39:41]

# Create a function to get the closest location

def closest_location(longitude, latitude):
    df_temp = q("select a.*, ((longitude - {}) * (longitude - {})) + ((latitude - {}) * (latitude - {})) d_squared from metadata_df a".format(longitude, longitude,  latitude, latitude))
    df_temp['d'] = df_temp['d_squared'].apply(lambda x: np.sqrt(x))
    return sqldf("select Descricao from df_temp order by d asc limit 1", locals()).Descricao[0]

closest_location(-8.618643,41.141412)

# Closest locations as column polyline_names

b = []
for z in df.iloc[0].POLYLINE.split("],["):
    a = z.replace("[","").replace("]","")
    split = a.split(",")
    x = split[0]
    y = split[1]
    # print(x, y)
    print()
    b.append(closest_location(x,y))
print(",".join(b))

#



df.head()

df.info()
df.dtypes

Zoom?
