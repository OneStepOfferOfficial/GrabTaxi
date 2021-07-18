from Dispatch import controller as controller
from Common.enum import *


def create_trip(location_pickup,location_dropoff,user_id):
    trip_id = controller.insert_trip(user_id,location_pickup,location_dropoff)
    return trip_id

def get_driver_id(trip_id):
    driver_id = controller.get_driver_id(trip_id)
    return driver_id

def get_driver_location(driver_id):
    driver_location = controller.get_driver_location(driver_id)
    return driver_location

def get_driver_detail(driver_id):
    driver_detail = controller.get_driver_detail(driver_id)
    return driver_detail

def update_trip_status(trip_id,status):
    controller.update_trip_status(trip_id,status)
    return

def sign_up_user(user_name,password,phone_number):
    controller.sign_up_user(user_name,password,phone_number)
    return

def verify_password_user(user_name,password):
    return controller.verify_password_user(user_name,password)

def get_user_id(user_name):
    return controller.get_user_id(user_name)

def sign_up_driver(driver_name, password, phone_number):
    controller.sign_up_driver(driver_name, password, phone_number)
    return
