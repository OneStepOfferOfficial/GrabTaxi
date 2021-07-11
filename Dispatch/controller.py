from Geo import view as geo_service
from Dispatch import DBhelper as DBhelper
import uuid

def store_trip(user_id,pickup_location,dropoff_location):
    trip_id = str(uuid.uuid1()).replace('-', '')
    DBhelper.insert_trip(trip_id,user_id,pickup_location,dropoff_location)
    return trip_id

def get_driver_id(trip_id):
    trip_detail = get_trip_detail(trip_id)
    nearest_drivers = geo_service.find_nearest_drivers(trip_detail)
    for driver in nearest_drivers:
        if query_driver(driver) == True:
            return driver.id

def query_driver(driver):
    '''
    :param driver:
    :return: True or False (Accept or not)
    '''

def get_trip_detail(trip_id):
    '''
    :param trip_id:
    :return: trip_detail=[trip_id,username,location_pickup,location_dropoff,time]
    '''
    pass
