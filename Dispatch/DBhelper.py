from Dispatch import config
import psycopg2

def build_connection():
    connection = psycopg2.connect(database=config.database_name,
                                  user=config.user_name,
                                  password=config.password,
                                  port=config.port,
                                  )
    return connection

def insert_trip(trip_id,user_id,pickup_location,dropoff_location):
    connection = build_connection()
    pickup_location = {pickup_location[0],pickup_location[1]}
    dropoff_location = {dropoff_location[0],dropoff_location[1]}
    cursor = connection.cursor()
    query = "INSERT INTO trip_table " \
            "(trip_id,user_id,status,pickup_location,dropoff_location)" \
            f"VALUES ('{trip_id}',{user_id},'created','{pickup_location}','{dropoff_location}');"
    cursor.execute(query)
    connection.commit()
    connection.close()

