from Geo import controller as controller

def find_nearest_drivers(pickup_location):
    return controller.find_nearest_drivers(pickup_location)

def get_driver_location(driver_id):
    return controller.get_driver_location(driver_id)

def update_driver_location(driver_id,longitude,latitude,with_redis):
    controller.update_driver_location(driver_id,longitude,latitude, with_redis)
