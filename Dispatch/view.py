from Dispatch import controler as controler
import uuid

def create_trip(location_pickup,location_dropoff,user_name):
    trip_id = str(uuid.uuid1()).replace('-', '')
    controler.store_trip(trip_id,user_name,location_pickup,location_dropoff)
    return trip_id

def get_driver_id(trip_id):
    driver_id = controler.get_driver_id(trip_id)
    return driver_id