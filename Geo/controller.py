from Geo.DBhelper import Helper
from Common.util import *
from Common.enum import *
from Geo import DBhelper as DBhelper

def get_search_zones(long,lati,distance,origin_zone):
    '''
    judge whether needs to search the drivers in the neighbour zones, if so put the zone into res
    :param long:
    :param lati:
    :param distance:
    :param zone:
    :return: A list of zones to search for nearby drivers
    '''
    final_result = [origin_zone]
    direction_zone_dict = {Direction.Right: find_zone(long, lati + distance), Direction.Left: find_zone(long, lati - distance),
                           Direction.Up: find_zone(long + distance, lati), Direction.Down: find_zone(long - distance, lati)}

    valid_directions = []
    for dir, zone in direction_zone_dict.items():
        if zone != origin_zone and zone != -1:
            valid_directions.append(dir)
            final_result.append(zone)

    if len(valid_directions) >= 2:
        neighbour_zone_direct_dict = {origin_zone + 9: (Direction.Left, Direction.Up), origin_zone + 11: (Direction.Right, Direction.Up),
                                      origin_zone - 11: (Direction.Down, Direction.Left), origin_zone - 9: (Direction.Down, Direction.Right)}

        for neighbour, dir_tuple in neighbour_zone_direct_dict.items():
            if dir_tuple[0] in valid_directions and dir_tuple[1] in valid_directions:
                final_result.append(neighbour)
    return final_result

def sort_nearest_drivers(drivers):
    '''
    sort the drivers according to their distance to the pickup location and return the top 10 drivers_id
    :param drivers
    :return: the top 10 drivers_id
    '''
    for index in range((len(drivers)-2)//2,-1,-1):
        bubble_down(drivers,index)
    return drivers[0:10]

def find_nearest_drivers(pickup_location,distance=4):
    drivers = []
    longitude = pickup_location[0]
    latitude = pickup_location[1]
    zone_of_pickup_location = find_zone(longitude,latitude)
    search_zones = get_search_zones(longitude,latitude,distance,zone_of_pickup_location)
    nearby_drivers = DBhelper.get_nearby_drivers(longitude,latitude,distance,search_zones)
    sorted_drivers = sort_nearest_drivers(nearby_drivers)
    return sorted_drivers

def get_driver_location(driver_id):
    driver_locaiton = DBhelper.get_driver_location(driver_id)
    return driver_locaiton
