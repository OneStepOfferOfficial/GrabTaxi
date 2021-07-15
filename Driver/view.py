from Driver import controller

def update_driver_location(driver_id,longitude,latitude):
    controller.update_driver_location(driver_id,longitude,latitude)

def update_all_drivers_locations():
    controller.update_all_drivers_locations()

update_all_drivers_locations()
