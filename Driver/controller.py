from Geo import view as Geo_service
from Common.util import *
import schedule
import time
import random

def update_driver_location(driver_id,longitude,latitude, with_redis):
    Geo_service.update_driver_location(driver_id,longitude,latitude, with_redis)

def update_all_drivers_locations(with_redis=True):
    '''
    every four seconds update the locations of drivers
    '''
    def job():
        for driver_id in range(1,20001):
            longitude = random.randint(0, 90)
            latitude = random.randint(0, 90)
            update_driver_location(driver_id, longitude, latitude, with_redis)
    schedule.every(1).seconds.do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)