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
    trip_status = DBhelper.get_trip_status(trip_id)
    if trip_status == "accepted":
        driver_id = DBhelper.get_driver_id(trip_id)
        return driver_id
    trip_detail = get_trip_detail(trip_id)
    pickup_location = trip_detail[1]
    # Keep finding nearest drivers and ask their decision
    while 1:
        nearest_drivers = geo_service.find_nearest_drivers(pickup_location)
        for driver in nearest_drivers:
            driver_answer = query_driver(driver.id,trip_detail)
            if driver_answer == "accepted":
                DBhelper.update_trip_status(trip_id,driver.id,status="accepted")
                DBhelper.update_driver_status(driver.id,status="busy")
                return driver.id
            elif driver_answer == "busy" or driver_answer == "already refused":
                continue
            elif driver_answer == "refused":
                DBhelper.update_trip_status(trip_id,driver.id,status="refused")
                continue

def query_driver(driver_id, trip_detail):
    '''
    Simulate the decision of driver
    :param driver_id, trip_detail
    :return: True or False (Accept or not)
    '''
    trip_id = trip_detail[0]
    driver_id_refused = DBhelper.get_driver_id_refused(trip_id)
    if driver_id_refused is not None and driver_id in driver_id_refused:
        return "already refused"
    driver_status = DBhelper.get_driver_status(driver_id)
    if driver_status == "busy":
        return "busy"
    return random.choice(["accepted","refused"])

def get_trip_detail(trip_id):
    '''
    :param trip_id:
    :return: trip_detail=[trip_id,pickup_location,dropoff_location]
    '''
    trip_detail = DBhelper.get_trip_detail(trip_id)
    return trip_detail

def get_driver_location(driver_id):
    driver_location = geo_service.get_driver_location(driver_id)
    return driver_location
