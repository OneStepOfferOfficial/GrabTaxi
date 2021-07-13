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
    pickup_location = "{"+f"{pickup_location[0]}"+","+f"{pickup_location[1]}"+"}"
    dropoff_location = "{"+f"{dropoff_location[0]}"+","+f"{dropoff_location[1]}"+"}"
    cursor = connection.cursor()
    query = "INSERT INTO trip_table " \
            "(trip_id,user_id,status,pickup_location,dropoff_location)" \
            f"VALUES ('{trip_id}',{user_id},'created',"+"'"+f"{pickup_location}"+"'"+","+"'"+f"{dropoff_location}"+"'"+");"
    cursor.execute(query)
    connection.commit()

def get_trip_detail(trip_id):
    cursor = connection.cursor()
    query = "SELECT pickup_location,dropoff_location FROM trip_table " \
            f"WHERE trip_id = '{trip_id}'"
    cursor.execute(query)
    connection.commit()
    res = cursor.fetchall()
    pickup_location = res[0][0]
    dropoff_location = res[0][1]
    return trip_id, pickup_location, dropoff_location

def create_trip_table():
    # create_trip_table
    cursor = connection.cursor()
    query = "CREATE TABLE trip_table(" \
            "trip_id TEXT PRIMARY KEY," \
            "user_id BIGINT," \
            "driver_id BIGINT," \
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP," \
            "finished_at TIMESTAMP," \
            "status TEXT," \
            "driver_id_refused BIGINT[]," \
            "pickup_location DECIMAL[]," \
            "dropoff_location DECIMAL[]" \
            ");"
    cursor.execute(query)
    connection.commit()

def create_user_table():
    # create_user_table
    cursor = connection.cursor()
    query = "CREATE TABLE user_table(" \
            "driver_id BIGSERIAL PRIMARY KEY," \
            "driver_name TEXT," \
            "phone_number VARCHAR(8)," \
            "password TEXT," \
            "trip_id TEXT);"
    cursor.execute(query)
    connection.commit()

def create_driver_table():
    # create_driver_table
    cursor = connection.cursor()
    query = "CREATE TABLE driver_table(" \
            "driver_id BIGSERIAL PRIMARY KEY," \
            "driver_name TEXT," \
            "status TEXT," \
            "phone_number VARCHAR(8)," \
            "password TEXT," \
            "trip_id TEXT);"
    cursor.execute(query)
    connection.commit()

def updata_trip_status(trip_id,driver_id,status):
    if status == "refused":
        query = "UPDATE trip_table " \
                f"SET driver_id_refused = driver_id_refused || {driver_id}::bigint " \
                f"WHERE trip_id = '{trip_id}';"
    else:
        query = "UPDATE trip_table " \
                f"SET driver_id = {driver_id} ," \
                f"status = '{status}' " \
                f"WHERE trip_id = '{trip_id}';"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

connection = build_connection()
