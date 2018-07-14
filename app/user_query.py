import numpy as np
import pandas as pd
import datetime as dt

# when is the next train coming?
df_schedule = pd.read_csv('train_schedules.csv')

# distances and travel time between stations
df_distances = pd.read_csv('df_distances.csv')

# number of passengers waiting per minute per station
df_queue = pd.read_csv('df_passengers_per_min_per_station.csv')

# check load factor: light, moderate, heavy
# note: currently hardcoded for demonstration purposes but can be
# computed using machine learning techniques given the datasets
# check load factor: light, moderate, heavy
def check_load_factor(time, is_raining=False, is_weekday=True):
    h = int(dt.datetime.fromtimestamp(time//1000).strftime('%H'))
    if (h >= 11 and h < 15) or (h >= 21):
        return 'lightly'
    elif (h < 7) or (h >= 9 and h < 11) or (h >= 15 and h < 16)\
        or (h >= 19 and h < 21):
        return 'moderately'
    else:
        return 'heavy'
    
get_time = lambda x: dt.datetime.fromtimestamp(x).time()
    
def query(time, station1, station2):
    scheds =  df_schedule.loc[df_schedule.loc[:, station1].apply(get_time)
                              >= get_time(time//1000), station1]
    
    if len(scheds) == 0:
        return ['There are no trains running at time. Operations will resume tomorrow at 4:00AM', 'Ingat po!']
    
    scheds = scheds.apply(lambda x: dt.datetime.fromtimestamp(x)\
                                      .strftime('%I:%M%p')).head().values
    
    target1 = df_distances.loc[(df_distances.start_station==station1)
                              & (df_distances.end_station==station2),
                              'travel_time']
    
    target2 = df_distances.loc[(df_distances.start_station==station2)
                              & (df_distances.end_station==station1),
                              'travel_time']
    
    travel_time = target1.values[0] if len(target1) != 0 else\
                    target2.values[0]
    
    queue_people = df_queue.loc[(df_queue.station==station1) &
                                (df_queue.Timestamp.apply(get_time)
                                 >= get_time(time//1000))]\
                            .sort_values('Timestamp').head(15).card_num.sum()
    
    
    queue = int((queue_people / 150) * 3 // 1)
    
    load_factor = check_load_factor(time)
    
    msg = 'Arrival schedules of the next '
    msg += f'five trains in {station1} station: '
    msg += ', '.join(scheds[:-1])
    msg += f', and {scheds[-1]}. '
    msg += f'Expected waiting time from station is {queue} minutes. '
    msg += f'Incoming trains are expected to be {load_factor} loaded. '
    msg += f'Total travel time from {station1} to {station2} '
    msg += f'is {int(np.round(travel_time))} minutes. '
    msg += 'Ingat po sa byahe!'
    
    return msg.split('. ')

