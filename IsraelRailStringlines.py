import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import time, timedelta, datetime, date
from math import radians, cos, sin, asin, sqrt

import rail_branches as rb

folder = 'gtfs_rail_18-01-2023'

d_date = date(2023,1,30)

direction = 1 # 0 for northbound 1 for southbound anything else for both

STOPSֹֹ_TO_REMOVE_BY = []

# Station and Train Selection

# example 1
STOPS_TO_FILTER_BY = rb.ayalon
STOPS_TO_DISPLAY = rb.herzelia + rb.ayalon + rb.airport + rb.jerusalem
STOPSֹֹ_TO_REMOVE_BY = rb.sharon

# # example 2
# STOPS_TO_FILTER_BY = rb.emek
# STOPS_TO_DISPLAY = rb.emek + rb.haifa + ['עתלית']
# direction = 2      # recommended

# # example 3
# STOPS_TO_FILTER_BY = rb.haifa + rb.hof + rb.herzelia + rb.ayalon 
# STOPS_TO_DISPLAY   = STOPS_TO_FILTER_BY
# STOPSֹֹ_TO_REMOVE_BY = rb.sharon

# # example 4 - Ayalon Third Track
# STOPS_TO_FILTER_BY = rb.sharon 
# STOPS_TO_DISPLAY   = rb.ayalon
# direction = 2      # recommended

STOPS_TO_DISPLAY.reverse()


def to_time(strtime):
    """
    This function converts a string representation of time to a time object.
    
    Parameters:
    strtime (str): A string representation of time in the format 'HH:MM:SS'
    
    Returns:
    time: A time object representing the given time.
    
    Raises:
    ValueError: If the hours in the given string representation of time are greater than 23.
    """
    return time.fromisoformat(strtime)

def to_date(strtime):
    """
    This function converts a string representation of time to a datetime object.
    
    Parameters:
    strtime (str): A string representation of time in the format 'HH:MM:SS'
    
    Returns:
    datetime: A datetime object representing the given time, combined with the current date.
    """
    global d_date
    d = d_date
    try:
        t = to_time(strtime)
    except ValueError:
        strtime = return_midnight_turnover(strtime)
        d = d_date.replace(day=d_date.day+1)
    return datetime.combine(d,to_time(strtime))

def add_date(strtime):
    return f"2017-01-01 {strtime}"
    
def get_station_y(int_num):
    global STOP_ID_TO_DISTACE_DICT
    return STOP_ID_TO_DISTACE_DICT[int_num]

def get_stop_name(stop_id):
    global STOPS
    return STOPS.loc[STOPS['stop_id']==stop_id,'stop_name'].to_numpy()[0][::-1]

def filter_data(data, column, filter_by):
    """returns filtered data by the specified column and list
    
    Args:
        data (pd.dataframe)
        column (str)
        filter_by (list)
    """
    if type(filter_by)==str or type(filter_by)==float or type(filter_by)==int:
        return data.loc[data[column]==filter_by,:]
    return data.loc[data[column].isin(filter_by),:]

def coord_distance(lat1, lat2, lon1, lon2):
     
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))
    
    r = 6378

    return(c * r)

def return_midnight_turnover(strtime):
    hour = int(strtime[:2])
    hour -= 24
    return f'{hour:02}{strtime[2:]}'


def stop_dist_from_stops(stop_id_lst):
    """
    This function calculates the distance between stops in a given list.
    
    Parameters:
    stop_id_lst (list): A list of stop IDs.
    
    Returns:
    list: A list of distances between each stop in the given list.
    """
    global STOPS
    stop_distaces_diff = [0]
    for s in range(len(stop_id_lst)-1):
        cur_stop = filter_data(STOPS,'stop_id',stop_id_lst[s])
        next_stop = filter_data(STOPS,'stop_id',stop_id_lst[s+1])
        lat1 = cur_stop.stop_lat
        lon1 = cur_stop.stop_lon
        lat2 = next_stop.stop_lat
        lon2 = next_stop.stop_lon
        cd = coord_distance(lat1, lat2, lon1, lon2)
        stop_distaces_diff.append(cd)

    stop_distaces = []
    for s in range(len(stop_distaces_diff)):
        stop_distaces.append(sum(stop_distaces_diff[:s+1]))
    if 42507 in stop_id_lst and 37388 in stop_id_lst:
        x = stop_id_lst.index(42507)
        y = stop_id_lst.index(37388)
        stop_distaces[x] = stop_distaces[y]
    return stop_distaces

def map_stop_name_to_id(lst):
    """
    Map a list of stop names to their corresponding stop IDs.

    Args:
        lst (list): A list of strings representing stop names.

    Returns:
        list: A list of strings representing stop IDs.

    Raises:
        KeyError: If a stop name in the input list is not found in the global dictionary NAME_TO_ID.
        TypeError: If not all elements in the input list are of type str.
    """
    global NAME_TO_ID
    
    if not all(isinstance(s, str) for s in lst):
        raise TypeError("All elements in the input list must be of type str")
    
    return [NAME_TO_ID[i] for i in lst]




stop_times = pd.read_csv(f"{folder}/stop_times.txt")
trips = pd.read_csv(f"{folder}/trips.txt")
calendar = pd.read_csv(f"{folder}/calendar.txt")
stops = pd.read_csv(f"{folder}/stops.txt")

STOPS = stops
STOP_TIMES = stop_times

NAME_TO_ID = dict(zip(stops['stop_name'],stops['stop_id']))
WEEKDAYS = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}



STOPS_TO_FILTER_BY = map_stop_name_to_id(STOPS_TO_FILTER_BY)
STOPS_TO_DISPLAY = map_stop_name_to_id(STOPS_TO_DISPLAY)
STOPSֹֹ_TO_REMOVE_BY = map_stop_name_to_id(STOPSֹֹ_TO_REMOVE_BY)

stop_distaces = stop_dist_from_stops(STOPS_TO_DISPLAY)

stop_names = [get_stop_name(i) for i in STOPS_TO_DISPLAY]

STOP_ID_TO_DISTACE_DICT = dict(zip(STOPS_TO_DISPLAY,stop_distaces))


weekday = WEEKDAYS[d_date.weekday()].lower()



filtered_trip_id = filter_data(stop_times,'stop_id',STOPS_TO_FILTER_BY).trip_id.drop_duplicates().to_numpy()


stops= stops.loc[stops['stop_id'].isin(STOPS_TO_DISPLAY),:]
stops


trips = trips[trips['trip_id'].isin(filtered_trip_id)]
filtered_service_id = trips.service_id.drop_duplicates().to_numpy()

filtered_calendar = calendar[calendar['service_id'].isin(filtered_service_id)]

s_date = int(d_date.isoformat().replace('-',''))
service_id_filter = (filtered_calendar[weekday]==1) & (filtered_calendar['start_date']<= s_date) & (filtered_calendar['end_date']>= s_date)
filtered_service_id = filtered_calendar[service_id_filter].service_id.drop_duplicates().to_numpy()

trips = trips[trips['service_id'].isin(filtered_service_id)]

if direction==0 or direction==1:
    trips = trips[trips['direction_id']==direction]


filtered_calendar[service_id_filter]

sp_trip_id = list(trips.trip_id.drop_duplicates().to_numpy())

stop_times = stop_times[stop_times['trip_id'].isin(sp_trip_id)]
stop_times = filter_data(stop_times,'stop_id',STOPS_TO_DISPLAY)

to_remove = []
for i in sp_trip_id:
    if len(list(filter_data(stop_times,'trip_id',i).trip_id.to_numpy()))<2:
        to_remove.append(i)

# filter out the trains that go through `STOPSֹֹ_TO_REMOVE_BY`
for i in sp_trip_id:
    d = filter_data(STOP_TIMES,'trip_id',i)
    stop_list = list(d.stop_id.to_numpy())
    flag_sharon = False
    for j in stop_list:
        if j in STOPSֹֹ_TO_REMOVE_BY:
            flag_sharon = True
    if flag_sharon:
        if i not in to_remove:
            to_remove.append(i)

for j in to_remove:
    sp_trip_id.remove(j)
    
stop_times = stop_times[stop_times['trip_id'].isin(sp_trip_id)]

stop_times[stop_times['departure_time']<"01:00:00"]

start_time = '07:00:00'
end_time   = '12:00:00'
crop = True

textRotation = -70

plt.rc('figure', figsize=(13, 7))


for i in sp_trip_id:
    whole_current_line = STOP_TIMES[STOP_TIMES['trip_id']==i]
    current_line = stop_times[(stop_times['trip_id']==i) & (stop_times['stop_id'].isin(STOPS_TO_DISPLAY))]
    current_line = current_line.sort_values(by='stop_sequence') 
    departure_times = current_line['departure_time'].apply(to_date).to_numpy()
    stop_ids = current_line['stop_id'].apply(get_station_y).to_numpy()
    plt.plot(departure_times,stop_ids,marker='o')
    
    if current_line.drop_off_type.sum()==0:
        # print starting station
        origin_station = whole_current_line.loc[whole_current_line.drop_off_type==1,:]
        originx = departure_times[0]
        originy = stop_ids[0]
        labelText = '  ' + origin_station.stop_id.apply(get_stop_name).to_numpy()[0] + '  '
        if not crop or (str(originx)[11:19] >= start_time and str(originx)[11:19] <= end_time):
            plt.text(originx,originy,labelText,rotation = textRotation,horizontalalignment='right', verticalalignment='center',rotation_mode='anchor')
    if current_line.pickup_type.sum()==0:
        # print ending station
        end_station = whole_current_line.loc[whole_current_line.pickup_type==1,:]
        endx = departure_times[-1]
        endy = stop_ids[-1]
        labelText = '  ' + end_station.stop_id.apply(get_stop_name).to_numpy()[0] + '  '
        if not crop or (str(endx)[11:19] >= start_time and str(endx)[11:19] <= end_time):
            plt.text(endx,endy,labelText,rotation = textRotation,rotation_mode='anchor',horizontalalignment='left', verticalalignment='center')
    


hours = mdates.HourLocator(interval = 1)
h_fmt = mdates.DateFormatter('%H:%M')
ax = plt.gca()
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)


title = f'{stop_names[0]} - {stop_names[-1]}'
plt.title(label=title,fontsize=30)

if crop:
    plt.xlim(to_date(start_time),to_date(end_time))

yPadding = (stop_distaces[-1]-stop_distaces[0])/5
plt.ylim(stop_distaces[0]-yPadding,stop_distaces[-1]+yPadding)

plt.gcf().autofmt_xdate()
plt.yticks(stop_distaces,stop_names)

plt.grid()

plt.show()