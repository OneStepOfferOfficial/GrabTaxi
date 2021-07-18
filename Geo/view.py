from Geo import controller as controller

def find_nearest_drivers(pickup_location):
    return controller.find_nearest_drivers(pickup_location)

def get_driver_location(driver_id):
    driver_location = controller.get_driver_location(driver_id)
    return driver_location