from Dispatch import controller as controller


def create_trip(location_pickup,location_dropoff,user_name):
    trip_id = controller.store_trip(user_name,location_pickup,location_dropoff)
    return trip_id

def get_driver_id(trip_id):
    driver_id = controller.get_driver_id(trip_id)
    return driver_id

def get_driver_location(driver_id):
    driver_location = controller.get_driver_location(driver_id)
    return driver_location
