"""Bike-Share"""

import math
from typing import List, TextIO

# For simplicity, we'll use "Station" in our type contracts to indicate that
# we mean a list containing station data.
#
# You can read "Station" in a type contract as:
#     List[int, str, float, float, int, int, int]
#
# where the values at each index represent the station data as described in the
# handout on Quercus.

# A set of constants, each representing a list index for station information.
ID = 0
NAME = 1
LATITUDE = 2
LONGITUDE = 3
CAPACITY = 4
BIKES_AVAILABLE = 5
DOCKS_AVAILABLE = 6
NO_KIOSK = 'SMART'

# For use in the get_lat_lon_distance helper function
EARTH_RADIUS = 6371

# SAMPLE DATA TO USE IN DOCSTRING EXAMPLES

SAMPLE_STATIONS = [
    [7090, 'Danforth Ave / Lamb Ave',
     43.681991, -79.329455, 15, 4, 10],
    [7486, 'Gerrard St E / Ted Reeve Dr',
     43.684261, -79.299332, 24, 5, 19],
    [7571, 'Highfield Rd / Gerrard St E - SMART',
     43.671685, -79.325176, 19, 14, 5]]

HANDOUT_STATIONS = [
    [7000, 'Ft. York / Capreol Crt.',
     43.639832, -79.395954, 31, 20, 11],
    [7001, 'Lower Jarvis St SMART / The Esplanade',
     43.647992, -79.370907, 15, 5, 10]]


# BEGIN HELPER FUNCTIONS

def is_number(value: str) -> bool:
    """Return True if and only if value represents a decimal number.

    >>> is_number('cscA08')
    False
    >>> is_number('  .08 ')
    True
    >>> is_number('+3.14159')
    True
    """

    return value.strip().lstrip('-+').replace('.', '', 1).isnumeric()


def get_lat_lon_distance(lat1: float, lon1: float,
                         lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by
    (lat1, lon1) and (lat2, lon2), rounded to the nearest metre.

    >>> get_lat_lon_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> get_lat_lon_distance(43.67, -79.37, 55.15, -118.8)
    3072.872
    """

    # This function uses the haversine function to find the distance between
    # two locations. You do NOT need to understand why it works.
    # You will just need to call on the function and work with what it returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return round(c * EARTH_RADIUS, 3)


# It isn't necessary to call this function to implement your bike_share.py
# functions, but you can use it to create larger lists for testing.
# See the main block below for an example of how to do that.
def csv_to_list(csv_file: TextIO) -> List[List[str]]:
    """Read and return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of csv_file.

    Docstring examples not given since results depend on data to be input.
    """

    # Read and discard header.
    csv_file.readline()

    data = []
    for line in csv_file:
        data.append(line.strip().split(','))
    return data


# END HELPER FUNCTIONS

# Data Conversion Function


def convert_data(data: List[list]) -> None:
    """Convert each string in data to an int if and only if it represents a
    whole number, and a float if and only if it represents a number that is not
    a whole number.

    >>> d = [['abc', '123', '45.6', 'car', 'Bike']]
    >>> convert_data(d)
    >>> d
    [['abc', 123, 45.6, 'car', 'Bike']]
    >>> d = [['ab2'], ['-123'], ['BIKES', '3.2'], ['3.0', '+4', '-5.0']]
    >>> convert_data(d)
    >>> d
    [['ab2'], [-123], ['BIKES', 3.2], [3, 4, -5]]
    """
    for lst in data:
        for num in range(len(lst)):
            if is_number(lst[num]):
                lst[num] = float(lst[num])
                if lst[num] == int(lst[num]):
                    lst[num] = int(lst[num])
                    
# Data Query Functions

def is_app_only(station: "Station") -> bool:
    """Return True if and only if the given station requires the use of an app.

    >>> is_app_only(SAMPLE_STATIONS[0])
    False
    >>> is_app_only(SAMPLE_STATIONS[2])
    True 
    """
    return NO_KIOSK in station[NAME]

def get_station_info(station_id: int, stations: List["Station"]) -> list:
    """Return a list containing the following information from stations
    about the station with id number station_id:
        - station name (str)
        - number of bikes available (int)
        - number of docks available (int)
        - whether or not the station has a kiosk (bool)
    (in this order)

    If station_id is not in stations, return an empty list.

    >>> get_station_info(7090, SAMPLE_STATIONS)
    ['Danforth Ave / Lamb Ave', 4, 10, True]
    >>> get_station_info(7571, SAMPLE_STATIONS)
    ['Highfield Rd / Gerrard St E - SMART', 14, 5, False]
    """
    result = []
    for info in stations:
        if station_id in info:
            result.append(info[NAME]) 
            result.append(info[BIKES_AVAILABLE])
            result.append(info[DOCKS_AVAILABLE])            
            result.append(not is_app_only(info))
    return result

def get_column_sum(index: int, stations: List["Station"]) -> int:
    """Return the sum of the values at the given index from each inner list
    of stations.

    Precondition: the items in stations at the position
                  that index refers to are ints.

    >>> get_column_sum(BIKES_AVAILABLE, SAMPLE_STATIONS)
    23
    >>> get_column_sum(DOCKS_AVAILABLE, SAMPLE_STATIONS)
    34
    """
    total = 0
    for station in stations:
        total = total + station[index]
    return total

def get_stations_with_kiosks(stations: List["Station"]) -> List[int]:
    """Return a list containing the station IDs for the stations in stations
    that have kiosks, in the same order as they appear in stations.

    >>> get_stations_with_kiosks(SAMPLE_STATIONS)
    [7090, 7486]
    >>> get_stations_with_kiosks(HANDOUT_STATIONS)
    [7000]
    """
    new_list = []
    for num in stations:
        if not is_app_only(num):
            new_list.append(num[ID])
    return new_list

def get_nearest_station(my_latitude: float, my_longitude: float,
                        stations: List['Station']) -> int:
    """Return the id of the station from stations that is nearest to the
    location given by my_latidute and my_longitude.

    In the case of a tie, return the ID of the last station in stations with
    that distance.

    Preconditions: len(stations) > 1

    >>> get_nearest_station(43.671134, -79.325164, SAMPLE_STATIONS)
    7571
    >>> get_nearest_station(43.674312, -79.299221, SAMPLE_STATIONS)
    7486
    """
    distance_1 = get_lat_lon_distance(my_latitude, my_longitude, \
    stations[0][LATITUDE], stations[0][LONGITUDE])
    station_id = 0
    for station in stations:
        distance_2 = (get_lat_lon_distance(my_latitude, my_longitude, \
        station[LATITUDE], station[LONGITUDE]))
        if distance_2 <= distance_1:
            distance_1 = distance_2
            station_id = station[ID]
    return station_id
    
# Data Modification Functions


def rent_bike(station_id: int, stations: List["Station"]) -> bool:
    """Update the available bike count and the docks available count
    for the station in stations with id station_id as if a single bike was
    removed, leaving an additional dock available. Return True if and only
    if the rental was successful.

    Precondition: station_id will appear in stations.

    >>> with_bike_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 4, 10]
    >>> station_id = with_bike_station[ID]
    >>> original_bikes_available = with_bike_station[BIKES_AVAILABLE]
    >>> original_docks_available = with_bike_station[DOCKS_AVAILABLE]
    >>> rent_bike(station_id, [with_bike_station])
    True
    >>> original_bikes_available - 1 == with_bike_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available + 1 == with_bike_station[DOCKS_AVAILABLE]
    True
    >>> no_bike_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 0, 15]
    >>> station_id = no_bike_station[ID]
    >>> original_bikes_available = no_bike_station[BIKES_AVAILABLE]
    >>> original_docks_available = no_bike_station[DOCKS_AVAILABLE]
    >>> rent_bike(station_id, [no_bike_station])
    False
    >>> original_bikes_available == no_bike_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available == no_bike_station[DOCKS_AVAILABLE]
    True
    """
    
    for info in stations:
        if station_id == info[ID]:
            if info[BIKES_AVAILABLE] >= 1:
                info[BIKES_AVAILABLE] = info[BIKES_AVAILABLE] - 1
                info[DOCKS_AVAILABLE] = info[DOCKS_AVAILABLE] + 1
                return True
    return False
        
def return_bike(station_id: int, stations: List["Station"]) -> bool:
    """Update the available bike count and the docks available count
    for station in stations with id station_id as if a single bike was added,
    making an additional dock unavailable. Return True if and only if the
    return was successful.

    Precondition: station_id will appear in stations.

    >>> available_dock_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 4, 10]
    >>> station_id = available_dock_station[ID]
    >>> original_bikes_available = available_dock_station[BIKES_AVAILABLE]
    >>> original_docks_available = available_dock_station[DOCKS_AVAILABLE]
    >>> return_bike(station_id, [available_dock_station])
    True
    >>> original_bikes_available + 1 == available_dock_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available - 1 == available_dock_station[DOCKS_AVAILABLE]
    True
    >>> no_dock_station = [7090, 'Danforth Ave / Lamb Ave', \
    43.681991, -79.329455, 15, 15, 0]
    >>> station_id = no_dock_station[ID]
    >>> original_bikes_available = no_dock_station[BIKES_AVAILABLE]
    >>> original_docks_available = no_dock_station[DOCKS_AVAILABLE]
    >>> return_bike(station_id, [no_dock_station])
    False
    >>> original_bikes_available == no_dock_station[BIKES_AVAILABLE]
    True
    >>> original_docks_available == no_dock_station[DOCKS_AVAILABLE]
    True
    """
    for info in stations:
        if station_id == info[ID]:
            if info[DOCKS_AVAILABLE] >= 1:
                info[BIKES_AVAILABLE] = info[BIKES_AVAILABLE] + 1
                info[DOCKS_AVAILABLE] = info[DOCKS_AVAILABLE] - 1
                return True
    return False

def upgrade_stations(threshold: int, num_bikes: int,
                     stations: List["Station"]) -> int:
    """Modify each station in stations that has a capacity that is less than
    threshold by adding num_bikes to the capacity and bikes available counts.
    Modify each station at most once.

    Return the total number of bikes that were added to the bike share network.

    Precondition: num_bikes >= 0

    >>> handout_copy = [HANDOUT_STATIONS[0][:], HANDOUT_STATIONS[1][:]]
    >>> upgrade_stations(25, 5, handout_copy)
    5
    >>> handout_copy[0] == HANDOUT_STATIONS[0]
    True
    >>> handout_copy[1] == [7001, 'Lower Jarvis St SMART / The Esplanade', \
                            43.647992, -79.370907, 20, 10, 10]
    True
    """
    for info in stations:
        if info[CAPACITY] < threshold:
            info[BIKES_AVAILABLE] = info[BIKES_AVAILABLE] + num_bikes
            info[CAPACITY] = info[CAPACITY] + num_bikes
    return num_bikes

if __name__ == '__main__':
    # leave this pass statement in place to ensure this if-body is not empty
    pass

    # Uncomment the following two statements to have your doctest examples run
    import doctest
    doctest.testmod()

    # To test your code with all of the stations data, uncomment the statements
    # that read data from the provided CSV file.
    stations_file = open('stations.csv')
    bike_stations = csv_to_list(stations_file)
    stations_file.close()
    convert_data(bike_stations)
    print(bike_stations)

    # And then uncomment and use statements like the following:
    print(get_station_info(7090, SAMPLE_STATIONS))
