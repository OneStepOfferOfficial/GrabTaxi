from Geo import config as config
import psycopg2

class Driver:
    def __init__(self,id,location):
        self.location = location
        self.id = id
        self.distance = None

    def calculate_distance(self,pickup_location):
        # calculate the distance to rider
        self.distance = (abs(float(pickup_location[0]-self.location[0]))**2 +
                         abs(float(pickup_location[1]-self.location[1]))**2)**0.5
        return self.distance


class Helper:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                                  user=config.user_name,
                                  password=config.password,
                                  port=config.port,
                                  )
        self.cursor = self.connection.cursor()

    def create_driver_location_table(self):
        query = "CREATE TABLE driver_location_table(" \
                "driver_id BIGSERIAL PRIMARY KEY," \
                "longitude DECIMAL," \
                "latitude DECIMAL," \
                "zone INT);"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data_into_table(self):
        query = "COPY driver_location_table(driver_id,longitude,latitude,zone)" \
                "FROM 'data.csv'" \
                "DELIMITER ','" \
                "CSV HEADER"
        self.cursor.execute(query)
        self.connection.commit()

    def separate_table(self):
        # build zone tables according to the driver position
        query = "CREATE TABLE driver_location_table(" \
                "driver_id BIGSERIAL PRIMARY KEY," \
                "longitude DECIMAL," \
                "latitude DECIMAL," \
                "zone INT);"
        self.cursor.execute(query)
        self.connection.commit()

    def get_nearby_drivers(self,longitude, latitude, distance, search_zones):
        nearby_drivers = []
        for zone in search_zones:
            query = (f"select * from driver_of_zone{zone} "
                     f"where longitude < {longitude + distance} "
                     f" and longitude > {longitude - distance}"
                     f" and latitude > {latitude - distance}"
                     f" and latitude < {latitude + distance}")
            self.cursor.execute(query)
            for record in self.cursor:
                driver = Driver(record[0], [record[1], record[2]])
                driver.calculate_distance([longitude, latitude])
                nearby_drivers.append(driver)
        return nearby_drivers
