import redis
from Redis import config

class Redis_helper:
    def __init__(self):
        self.redis = redis.Redis(host=config.host, port=config.port, decode_responses=config.decode_responses)

    def get_driver_location_redis(self, driver_id):
        longitude, latitude = self.redis.hmget(driver_id, "longitude", "latitude")
        try:
            return float(longitude), float(latitude)
        except :
            return None, None

    def set_driver_location_redis(self, driver_id,longitude,latitude):
        self.redis.hmset(driver_id,{"longitude":longitude, "latitude":latitude})

    def delete_driver_location_redis(self, driver_id):
        self.redis.delete(driver_id)



