from Redis import redis_helper
from Geo import DBhelper as Geo_DBhelper


def get_driver_location(driver_id):
    longitude, latitude = redis_helper.get_driver_location_redis(driver_id)
    if longitude and latitude:
        return longitude, latitude
    longitude, latitude = Geo_DBhelper.get_driver_location(driver_id)
    redis_helper.set_driver_location_redis(driver_id, longitude, latitude)
    return longitude, latitude

def get_driver_location_without_database(driver_id):
    return redis_helper.get_driver_location_redis(driver_id)

def update_driver_location(driver_id, longitude, latitude):
    redis_helper.set_driver_location_redis(driver_id, longitude, latitude)

def delete_driver_location(driver_id):
    redis_helper.delete_driver_location_redis(driver_id)

