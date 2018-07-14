import numpy as np
import pandas as pd

def get_closest_station(my_lat, my_long):
    df_stations = pd.read_csv('LRT1 Station Coordinates.csv', index_col=0)
    saved_i=0

    for i, each in enumerate(df_stations.index):
        dist = np.linalg.norm([my_lat, my_long] - df_stations.loc[each,['lat','long']])
        if i == 0: min_dist = dist
        if min_dist > dist:
            saved_i = i
            min_dist = dist

    return df_stations.index[saved_i]
