from Geo.DBhelper import Helper
from Common.util import *


DBhelper = Helper()

def update_driver_location(driver_id,longitude,latitude):
    DBhelper.update_driver_location(driver_id,longitude,latitude)

