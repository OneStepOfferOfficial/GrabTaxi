from Geo import config as config
from Common.util import *
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
        for zone in range(100):
            query = f"CREATE TABLE driver_of_zone{zone} AS " \
                    f"SELECT * from driver_location_table " \
                    f"WHERE zone={zone}"
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

    def update_driver_location(self,driver_id,longitude,latitude):
        query = ("SELECT zone FROM driver_location_table "
                 f"WHERE driver_id = {driver_id} ")
        self.cursor.execute(query)
        origin_zone = self.cursor.fetchall()[0][0]
        new_zone = find_zone(longitude,latitude)
        if origin_zone == new_zone:
            # update the driver location in the corresponding driver_of_zone_table
            query = (f"UPDATE driver_of_zone{origin_zone} "
                     f"SET longitude = {longitude},"
                     f"latitude = {latitude} "
                     f"WHERE driver_id = {driver_id}")
            self.cursor.execute(query)
            self.connection.commit()
        else:
            # delete the driver location record in the original driver_of_zone(origin_zone)_table
            query = (f"DELETE FROM driver_of_zone{origin_zone} "
                     f"WHERE driver_id = {driver_id};")
            self.cursor.execute(query)
            self.connection.commit()
            # insert the driver location record in the driver_of_zone(new_zone) table
            query = (f"INSERT INTO driver_of_zone{new_zone} "
                     f"VALUES ('{driver_id}','{longitude}','{latitude}','{new_zone}')")
            self.cursor.execute(query)
            self.connection.commit()
        # update the driver location in the driver_location_table
        query = ("UPDATE driver_location_table "
                 f"SET longitude = {longitude},"
                 f"latitude = {latitude}, "
                 f"zone = {new_zone}"
                 f"WHERE driver_id = {driver_id}")
        self.cursor.execute(query)
        self.connection.commit()

    def get_driver_location(self,driver_id):
        query = "SELECT longitude, latitude FROM driver_location_table " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        driver_location = self.cursor.fetchall()[0]
        return driver_location


