from Geo.DBhelper import Helper
from Common.util import *
import schedule
import time
import random

DBhelper = Helper()

def update_driver_location(driver_id,longitude,latitude):
    DBhelper.update_driver_location(driver_id,longitude,latitude)

def update_all_drivers_locations():
    '''
    every four seconds update the locations of drivers
    '''
    def job():
        for driver_id in range(1,20001):
            longitude = random.randint(0, 90)
            latitude = random.randint(0, 90)
            update_driver_location(driver_id, longitude, latitude)
        print("I am done with updating driver locations")

    schedule.every(3).seconds.do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)
