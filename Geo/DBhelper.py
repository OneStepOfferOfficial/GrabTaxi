from Geo import config as config
import psycopg2

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

