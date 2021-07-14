from Geo import view as geo_service
from Dispatch.DBhelper import Helper
import random
import uuid

DBhelper = Helper()

def store_trip(user_id,pickup_location,dropoff_location):
    trip_id = str(uuid.uuid1()).replace('-', '')
    DBhelper.insert_trip(trip_id,user_id,pickup_location,dropoff_location)
    return trip_id

def get_driver_id(trip_id):
    trip_detail = get_trip_detail(trip_id)
    pickup_location = trip_detail[1]
    nearest_drivers = geo_service.find_nearest_drivers(pickup_location)
    for driver in nearest_drivers:
        if query_driver(driver.id,trip_detail) == True:
            DBhelper.update_trip_status(trip_id,driver.id,status="accepted")
            return driver.id
        else:
            DBhelper.update_trip_status(trip_id,driver.id,status="refused")


def query_driver(driver_id, trip_detail):
    '''
    Simulate the decision of driver
    :param driver_id, trip_detail
    :return: True or False (Accept or not)
    '''
    return random.choice([True,False])

def get_trip_detail(trip_id):
    '''
    :param trip_id:
    :return: trip_detail=[trip_id,pickup_location,dropoff_location]
    '''
    trip_detail = DBhelper.get_trip_detail(trip_id)
    return trip_detail


