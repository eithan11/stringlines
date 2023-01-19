import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import time, timedelta, datetime, date
from math import radians, cos, sin, asin, sqrt

def to_time(strtime):
    return time.fromisoformat(strtime)

def to_date(strtime):
    d = date(2000,1,1)
    try:
        t = to_time(strtime)
    except ValueError:
        strtime = return_midnight_turnover(strtime)
        d = date(2000,1,2)
    return datetime.combine(d,to_time(strtime))

def add_date(strtime):
    return f"2017-01-01 {strtime}"
    
def get_station_y(int_num):
    global stations_dict
    return stations_dict[int_num]

def get_stop_name(stop_id):
    global stops
    return stops[stops['stop_id']==stop_id]['stop_name'].to_numpy()[0][::-1]

def filter_data(data, column, filter_by):
    """returns filtered data by the specified column and list
    
    Args:
        data (pd.dataframe)
        column (str)
        filter_by (list)
    """
    if type(filter_by)==str or type(filter_by)==float or type(filter_by)==int:
        return data[data[column]==filter_by]
    return data[data[column].isin(filter_by)]

def coord_distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def return_midnight_turnover(strtime):
    hour = int(strtime[:2])
    hour -= 24
    return f'{hour:02}{strtime[2:]}'

def stop_dist_from_stops(sp_stop_id):
    stop_distaces_diff = [0]
    for s in range(len(sp_stop_id)-1):
        cur_stop = filter_data(stops,'stop_id',sp_stop_id[s])
        next_stop = filter_data(stops,'stop_id',sp_stop_id[s+1])
        lat1 = cur_stop.stop_lat
        lon1 = cur_stop.stop_lon
        lat2 = next_stop.stop_lat
        lon2 = next_stop.stop_lon
        if list(next_stop.stop_id==37388)[0]:
            cd = 0
        else:
            cd = coord_distance(lat1, lat2, lon1, lon2)
        stop_distaces_diff.append(cd)

    stop_distaces = []
    for s in range(len(stop_distaces_diff)):
        stop_distaces.append(sum(stop_distaces_diff[:s+1]))
    return stop_distaces

def shorten_trip_id_lst(sp_trip_id):
    to_remove = []
    for i in sp_trip_id:
        if len(list(filter_data(stop_times,'trip_id',i).trip_id.to_numpy()))<2:
            to_remove.append(i)

    # filter out the trains on hasharon loop without filtering out the trains to jerusalem
    for i in sp_trip_id:
        d = filter_data(stop_times,'trip_id',i)
        stop_list = list(d.stop_id.to_numpy())
        flag_sharon = False
        for j in stop_list:
            if j in hashron_loop_stop_ids:
                flag_sharon = True
        if flag_sharon:
            if i not in to_remove:
                to_remove.append(i)

    for j in to_remove:
        sp_trip_id.remove(j)

class Stringlines:
    def __init__(self,control_stop, sp_stop_id=[], weekday='sunday',direction=0,start_time='00:00:00', end_time='23:59:59',title='') -> None:
        self.control_stop = control_stop
        self.sp_stop_id = sp_stop_id
        self.weekday = weekday
        self.direction = direction
        self.start_time = start_time
        self.end_time = end_time
        if start_time=='00:00:00' and end_time=='23:59:59':
            self.crop = False
        else:
            self.crop = True
        if self.sp_stop_id==[]:
            self.sp_stop_id = self.control_stop
        self.stop_distaces = stop_dist_from_stops(self.sp_stop_id)
        self.stop_names = [get_stop_name(i) for i in self.sp_stop_id]
        self.stations_dict = dict(zip(self.sp_stop_id,self.stop_distaces))
        if title:
            self.title = title
        else:
            self.title = f'{self.stop_names[0]} - {self.stop_names[-1]}'
        
        self.calculate()
            
        
    def get_station_y(self, lst_of_num):
        ret_lst = []
        for i in lst_of_num:
            ret_lst.append(self.stations_dict[i])
        return ret_lst

    def show(self):
        for i in self.sp_trip_id:
            self.current_line = self.stop_times[self.stop_times['trip_id']==i]
            self.current_line = self.current_line[self.current_line['stop_id'].isin(self.sp_stop_id)]
            self.current_line.sort_values(by='stop_sequence', inplace = True) 
            self.departure_time = self.current_line['departure_time'].apply(to_date).to_numpy()
            self.stops_y = self.get_station_y(self.current_line.stop_id.to_numpy())
            plt.plot(self.departure_time,self.stops_y,marker='o')


        hours = mdates.HourLocator(interval = 1)
        h_fmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_locator(hours)
        plt.gca().xaxis.set_major_formatter(h_fmt)

        plt.title(label=self.title,fontsize=25)

        if self.crop:
            plt.xlim(to_date(self.start_time),to_date(self.end_time))

        plt.gcf().autofmt_xdate()
        plt.yticks(self.stop_distaces,self.stop_names)
        plt.rc('figure', figsize=(20, 10))
        plt.grid()

        plt.show()


    def calculate(self):
        

        self.my_trip_ids = filter_data(stop_times,'stop_id',self.control_stop).trip_id.drop_duplicates().to_numpy()

        self.trips = trips[trips['trip_id'].isin(self.my_trip_ids)]
        self.my_service_ids = trips.service_id.drop_duplicates().to_numpy()


        self.my_calendar = calendar[calendar['service_id'].isin(self.my_service_ids)]
        self.my_service_ids = self.my_calendar[self.my_calendar[self.weekday]==1].service_id.drop_duplicates().to_numpy()

        self.trips = self.trips[self.trips['service_id'].isin(self.my_service_ids)]

        if self.direction==0 or self.direction==1:
            self.trips = self.trips[self.trips['direction_id']==self.direction]
        
        self.sp_trip_id = list(self.trips.trip_id.drop_duplicates().to_numpy())

        self.stop_times = stop_times[stop_times['trip_id'].isin(self.sp_trip_id)]
        self.stop_times = filter_data(self.stop_times,'stop_id',self.sp_stop_id)

        shorten_trip_id_lst(self.sp_trip_id)

        self.stop_times = self.stop_times[self.stop_times['trip_id'].isin(self.sp_trip_id)]

        self.T0 = to_date(self.stop_times.departure_time.min())

class Stringline:
    def __init__(self) -> None:
        pass


folder = 'gtfs_rail_only2'

stop_times = pd.read_csv(f"{folder}/stop_times.txt")
trips = pd.read_csv(f"{folder}/trips.txt")
calendar = pd.read_csv(f"{folder}/calendar.txt")
stops = pd.read_csv(f"{folder}/stops.txt")


hashron_loop_stop_ids = [37296, 37302, 37304, 37352, 37354, 37356, 42416, 42417]
