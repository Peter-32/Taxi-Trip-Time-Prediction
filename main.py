import numpy as np
import pandas as pd
from pandasql import sqldf
import time
import re
#pd.options.display.html.table_schema = True
#pd.options.display.max_rows = None
q = lambda q: sqldf(q, globals())

class ETL:

    def __init__(self, user):
        self.user = user
        self.df, self.metadata_df, self.train_df, self.test_df = None, None, None, None

    def execute(self):
        self.set_datasets()
        self.set_time_taken()
        self.fix_metadata_df()

    def set_datasets(self):
        if self.user == "peter":
            path = "/Users/peterjmyers/work/Taxi-Trip-Time-Prediction/data/"
        elif self.user == "cheryl":
            path = "/Users/cheryljose/Documents/Projects/all/"
        self.df = pd.read_csv('{}train.csv'.format(path), sep=",", nrows=10)
        self.metadata_df = pd.read_csv('{}metaData_taxistandsID_name_GPSlocation.csv'.format(path), sep=",")
        self.train_df = pd.read_csv('{}train.csv'.format(path), sep=",", nrows=10)
        self.test_df = pd.read_csv('{}test.csv'.format(path), sep=",", nrows=10)

    def set_time_taken(self):
        self.df['polyline_length'] = self.df['POLYLINE'].apply(lambda x: len(x.split("],[")))
        self.df['time_taken'] = self.df['polyline_length'].apply(lambda x: (x - 1) * 15)
        self.df.head()

    def fix_metadata_df(self):
        self.metadata_df['Latitude'][40] = 41.163066654
        self.metadata_df['Longitude'][40] = -8.67598304213
        self.metadata_df.iloc[39:41]

etl = ETL("peter")
etl = ETL("cheryl")
etl.execute()
df, metadata_df = etl.df, etl.metadata_df

def closest_location(longitude, latitude):
    df_temp = q("select a.*, ((longitude - {}) * (longitude - {})) + ((latitude - {}) * (latitude - {})) d_squared from metadata_df a".format(longitude, longitude,  latitude, latitude))
    df_temp.loc[:, 'd'] = df_temp['d_squared'].apply(lambda x: np.sqrt(x))
    return sqldf("select Descricao from df_temp order by d asc limit 1", locals()).Descricao[0]

# TODO: Fix closest location to use this code: (load the tree once and save it outside this function)
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.html
# >>> from scipy import spatial
# >>> airports = [(10,10),(20,20),(30,30),(40,40)]
# >>> tree = spatial.KDTree(airports)
# >>> tree.query([(21,21)])
# (array([ 1.41421356]), array([1]))
that will do it


closest_location(-8.618643,41.141412)

j = 0
polyline_names_list = []
for i in range(df.shape[0]):
    polyline_names = []
    for coordinates in df.iloc[i].POLYLINE.split("],["):
        coordinates = coordinates.replace("[", "").replace("]", "")

        x, y = coordinates.split(",")[0], coordinates.split(",")[1]
        polyline_names.append(closest_location(x, y))
        # j += 1
    # polyline_names_list.append(polyline_names)
    print(i)


running closest_location hundreds of times is slow
slow
    fast still
that's fast
j=332
#df.loc[:, 'd'] = polyline_names_list
#df.head()

# can probably speed it up at some point.  maybe closest_location

.03 seconds times 300 times is 9 seconds
ok
hmm

data structures and algorithms problem

????ho

Should we move on or try to speed up this lookup?
We should sort the latitude and longitude for quicker searches
what do you think would be better ?
why not radix
no i am not sure. i just remember you told it's fast
yeah maybe, I forget
hmm
the radix I know about is a sort, we could sort it once.  We need to do thousands of searches.  I'll try googling
binary search for close latitudes or longitudes maybe
how about we search what would be good ways to do a quicker search and come back tomorrow with ideas ?
we can work late tomorrow
okay okay :)

put that code here :)
i will refer it
thank you

is this saved ??

yeah. pushing to github now
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.html
# >>> from scipy import spatial
# >>> airports = [(10,10),(20,20),(30,30),(40,40)]
# >>> tree = spatial.KDTree(airports)
# >>> tree.query([(21,21)])
# (array([ 1.41421356]), array([1]))
# Where 1.41421356 is the distance between the queried point
# the nearest neighbour and 1 is the index of the neighbour.

that will do it

metadata_df.head()
ID	Descricao	Latitude	Longitude
# 0	1	Agra	41.1771457135	-8.609670
# 1	2	Alameda	41.15618964	-8.591064
# 2	3	Aldoar	41.1705249231	-8.665876
# 3	4	Alfândega	41.1437639911	-8.621803
# 4	5	Amial	41.1835097223	-8.612726
