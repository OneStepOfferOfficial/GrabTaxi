from Geo import view as geo_service
from Common.enum import *
import random
import uuid
from Dispatch import DBhelper as DBhelper
from Redis import controller as redis


def insert_trip(user_id,pickup_location,dropoff_location):
    trip_id = str(uuid.uuid1()).replace('-', '')
    DBhelper.insert_trip(trip_id,user_id,pickup_location,dropoff_location)
    return trip_id

def get_driver_id(trip_id):
    trip_status = DBhelper.get_trip_status(trip_id)
    if trip_status == Trip_status.Accepted:
        driver_id = DBhelper.get_driver_id(trip_id)
        return driver_id
    trip_detail = get_trip_detail(trip_id)
    pickup_location = trip_detail[0]
    # Keep finding nearest drivers and ask their decision
    while True:
        nearest_drivers = geo_service.find_nearest_drivers(pickup_location)
        for driver in nearest_drivers:
            driver_answer = query_driver(driver.id,trip_id,trip_detail)
            if driver_answer == Driver_answer.Accept:
                DBhelper.update_trip_status(trip_id,status=Trip_status.Accepted)
                DBhelper.update_trip_driver(trip_id,driver.id)
                DBhelper.update_driver_status(driver.id,status=Driver_status.Not_available)
                return driver.id
            elif driver_answer == Driver_answer.Already_refused or driver_answer == Driver_answer.Busy:
                continue
            elif driver_answer == Driver_answer.Refuse:
                DBhelper.update_driver_id_refused(trip_id,driver.id)
                continue

def query_driver(driver_id,trip_id, trip_detail):
    '''
    Simulate the decision of driver
    :param driver_id, trip_id, trip_detail
    :return: Driver_answer
    '''
    driver_id_refused = DBhelper.get_driver_id_refused(trip_id)
    if driver_id_refused is not None and driver_id in driver_id_refused:
        return Driver_answer.Already_refused
    driver_status = DBhelper.get_driver_status(driver_id)
    if driver_status == Driver_status.Not_available:
        return Driver_answer.Busy
    return random.choice([Driver_answer.Accept,Driver_answer.Refuse])

def get_trip_detail(trip_id):
    '''
    :param trip_id:
    :return: trip_detail=[pickup_location,dropoff_location]
    '''
    trip_detail = DBhelper.get_trip_detail(trip_id)
    return trip_detail

def get_driver_location(driver_id):
    return redis.get_driver_location(driver_id)

def get_driver_detail(driver_id):
    driver_detail = DBhelper.get_driver_detail(driver_id)
    return driver_detail

def update_trip_status(trip_id,status):
    if status == Trip_status.Ongoing:
        DBhelper.update_trip_status(trip_id,status)
    elif status == Trip_status.Finished:
        DBhelper.update_trip_status(trip_id,status)
        driver_id = DBhelper.get_driver_id(trip_id)
        DBhelper.update_driver_status(driver_id,Driver_status.Available)
        redis.delete_driver_location(driver_id)
        
def verify_password_user(user_name,password):
    real_password = DBhelper.get_password_user(user_name)
    if real_password == password:
        return True
    else:
        return False

def get_user_id(user_name):
    user_id = DBhelper.get_user_id(user_name)
    return user_id

def sign_up_user(user_name,password,phone_number):
    DBhelper.insert_user(user_name,password,phone_number)

def sign_up_driver(driver_name,password,phone_number):
    DBhelper.insert_driver(driver_name,password,phone_number)

