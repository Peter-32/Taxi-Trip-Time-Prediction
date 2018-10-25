import numpy as np
import pandas as pd
from pandasql import sqldf
from scipy import spatial
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
        self.df = pd.read_csv('{}train.csv'.format(path), sep=",", nrows=30)
        self.metadata_df = pd.read_csv('{}metaData_taxistandsID_name_GPSlocation.csv'.format(path), sep=",")
        self.train_df = pd.read_csv('{}train.csv'.format(path), sep=",", nrows=30)
        self.test_df = pd.read_csv('{}test.csv'.format(path), sep=",", nrows=30)

    def set_time_taken(self):
        self.df['polyline_length'] = self.df['POLYLINE'].apply(lambda x: len(x.split("],[")))
        self.df['time_taken'] = self.df['polyline_length'].apply(lambda x: (x - 1) * 15)
        self.df.head()

    def fix_metadata_df(self):
        self.metadata_df['Latitude'][40] = 41.163066654
        self.metadata_df['Longitude'][40] = -8.67598304213
        self.metadata_df.iloc[39:41]
1+1
etl = ETL("peter")
etl = ETL("cheryl")
etl.execute()
df, metadata_df = etl.df, etl.metadata_df

coordinates = metadata_df.values[:,2:].astype(float)
locations = metadata_df.values[:,1]
coordinates
locations
coordinates.shape
locations.shape
tree = spatial.KDTree(coordinates)

#Running in a different notebook
#you here ?

def closest_location(longitude, latitude):
    return locations[tree.query([(longitude, latitude)])[1][0]]

closest_location(-8.618643,41.141412)

def closest_location2(longitude, latitude):
    return locations[tree.query([(longitude, latitude)])[1][0]]
#df_temp = q("select a.*, ((longitude - {}) * (longitude - {})) + ((latitude - {}) * (latitude - {})) d_squared from metadata_df a".format(longitude, longitude,  latitude, latitude))
#df_temp.loc[:, 'd'] = df_temp['d_squared'].apply(lambda x: np.sqrt(x))
#sqldf("select Descricao from df_temp order by d asc limit 1", locals()).Descricao[0]

closest_location2(-8.618643,41.141412)


# Closest locations as column polyline_names

# 1) Populate the list polyline_names_list


polyline_names_list = []
for i in range(df.shape[0]):
    polyline_names = []
    for coordinates in df.iloc[i].POLYLINE.split("],["):
        coordinates = coordinates.replace("[", "").replace("]", "")
        x, y = coordinates.split(",")[0], coordinates.split(",")[1]
        polyline_names.append(closest_location(x, y))
    polyline_names_list.append(polyline_names)
    print("a")
df.loc[:, 'd'] = polyline_names_list
df.head()






We can add the code below `closest_location`:

            https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.html
            # >>> from scipy import spatial
            # >>> airports = [(10,10),(20,20),(30,30),(40,40)]
            # >>> tree = spatial.KDTree(airports)
            # >>>
            # (array([ 1.41421356]), array([1]))




#df_temp = q("select a.*, ((longitude - {}) * (longitude - {})) + ((latitude - {}) * (latitude - {})) d_squared from metadata_df a".format(longitude, longitude,  latitude, latitude))
#df_temp.loc[:, 'd'] = df_temp['d_squared'].apply(lambda x: np.sqrt(x))
#sqldf("select Descricao from df_temp order by d asc limit 1", locals()).Descricao[0]
