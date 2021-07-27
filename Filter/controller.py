from Filter import filter
from Geo import DBhelper as Geo_DBhelper

def get_driver_location(driver_id):
    longitude, latitude = filter.get_driver_location_redis(driver_id)
    return longitude, latitude

def update_driver_location(driver_id, longitude, latitude):
    filter.set_driver_location_redis(driver_id, longitude, latitude)

def delete_driver_location(driver_id):
    filter.delete_driver_location_redis(driver_id)
