from Geo import view as geo_service

def store_trip(trip_id,user_name,location_pickup,location_dropoff):
    pass

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