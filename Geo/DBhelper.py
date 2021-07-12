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

def build_connection():
    connection = psycopg2.connect(database=config.database_name,
                                  user=config.user_name,
                                  password=config.password,
                                  port=config.port,
                                  )
    return connection

def create_driver_location_table():
    # create_driver_table
    connection = build_connection()
    cursor = connection.cursor()
    query = "CREATE TABLE driver_location_table(" \
            "driver_id BIGSERIAL PRIMARY KEY," \
            "longitude DECIMAL," \
            "latitude DECIMAL," \
            "zone INT);"
    cursor.execute(query)
    connection.commit()
    connection.close()

def insert_data_into_table():
    connection = build_connection()
    cursor = connection.cursor()
    query = "COPY driver_location_table(driver_id,longitude,latitude,zone)" \
            "FROM 'D:\Desktop\Documents\OneStep Project\Grab Project\GrabTaxi\Geo\data.csv'" \
            "DELIMITER ','" \
            "CSV HEADER"
    cursor.execute(query)
    connection.commit()
    connection.close()

def separate_table():
    connection = build_connection()
    cursor = connection.cursor()
    for i in range(90):
        query = f"CREATE TABLE driver_of_zone{i} AS " \
                f"SELECT *" \
                f"FROM driver_location_table " \
                f"WHERE zone = {i}"
        cursor.execute(query)
        connection.commit()
    connection.close()

def get_nearby_drivers(longitude,latitude,distance,search_zones):
    nearby_drivers = []
    connection = build_connection()
    cursor = connection.cursor()
    for zone in search_zones:
        query = (f"select * from driver_of_zone{zone} "
                 f"where longitude < {longitude+distance} "
                 f" and longitude > {longitude-distance}"
                 f" and latitude > {latitude-distance}"
                 f" and latitude < {latitude+distance}")
        cursor.execute(query)
        for record in cursor:
            driver = Driver(record[0],[record[1],record[2]])
            driver.calculate_distance([longitude,latitude])
            nearby_drivers.append(driver)
    return nearby_drivers