from Dispatch import config
import psycopg2
from Common.enum import *
from Common.decorator import *


class Helper:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                                           user=config.user_name,
                                           password=config.password,
                                           port=config.port,
                                           )
        self.cursor = self.connection.cursor()

    @log_error_db
    def insert_trip(self, trip_id, user_id, pickup_location, dropoff_location):
        pickup_location = "{" + f"{pickup_location[0]}" + "," + f"{pickup_location[1]}" + "}"
        dropoff_location = "{" + f"{dropoff_location[0]}" + "," + f"{dropoff_location[1]}" + "}"
        query = "INSERT INTO trip_table " \
                "(trip_id,user_id,status,pickup_location,dropoff_location)" \
                f"VALUES ('{trip_id}',{user_id},1," + "'" + f"{pickup_location}" + "'" + "," + "'" + f"{dropoff_location}" + "'" + "); "
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def insert_driver(self, driver_name, password, phone_number):
        query = "INSERT INTO driver_table " \
                "(driver_name,password,phone_number)" \
                f"VALUES ('{driver_name}','{password}', '{phone_number}');"
        self.cursor.execute(query)
        self.connection.commit()
        # reset the max id to avoid id conflict
        query = "select setval('driver_table_driver_id_seq', (select max(driver_id) from driver_table));"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def insert_user(self, user_name, password, phone_number):
        query = "INSERT INTO user_table " \
                "(user_name,password,phone_number)" \
                f"VALUES ('{user_name}','{password}', '{phone_number}');"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def get_trip_detail(self, trip_id):
        query = "SELECT pickup_location,dropoff_location FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        self.connection.commit()
        res = self.cursor.fetchall()
        pickup_location = res[0][0]
        dropoff_location = res[0][1]
        return pickup_location, dropoff_location

    @log_error_db
    def create_trip_table(self):
        # create_trip_table
        query = "CREATE TABLE trip_table(" \
                "trip_id TEXT PRIMARY KEY," \
                "user_id BIGINT," \
                "driver_id BIGINT," \
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP," \
                "finished_at TIMESTAMP," \
                "status smallint," \
                "driver_id_refused BIGINT[]," \
                "pickup_location DECIMAL[]," \
                "dropoff_location DECIMAL[]" \
                ");"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def insert_data_into_driver_table(self):
        query = "COPY driver_table(driver_id,driver_name,status,phone_number,password)" \
                "FROM 'driver_data.csv'" \
                "DELIMITER ','" \
                "CSV HEADER"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def create_driver_table(self):
        # create_driver_table
        query = "CREATE TABLE driver_table(" \
                "driver_id BIGSERIAL PRIMARY KEY," \
                "driver_name TEXT," \
                "status smallint," \
                "phone_number VARCHAR(8)," \
                "password TEXT);"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def create_user_table(self):
        # create_user_table
        query = "CREATE TABLE user_table(" \
                "user_id BIGSERIAL PRIMARY KEY," \
                "user_name TEXT," \
                "phone_number VARCHAR(8)," \
                "password TEXT);"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def update_trip_status(self, trip_id, status):
        if type(status) != int:
            status = status.value
        query = "UPDATE trip_table " \
                f"SET status = {status}" \
                f"WHERE trip_id = '{trip_id}';"
        self.cursor.execute(query)
        self.connection.commit()
        if status == 4:  # if the trip is finished, edit the finish_at column.
            query = "UPDATE trip_table " \
                    f"SET finished_at = CURRENT_TIMESTAMP " \
                    f"WHERE trip_id = '{trip_id}'"
            self.cursor.execute(query)
            self.connection.commit()

    @log_error_db
    def update_trip_driver(self, trip_id, driver_id):
        query = "UPDATE trip_table " \
                f"SET driver_id = {driver_id}" \
                f"WHERE trip_id = '{trip_id}';"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def update_driver_id_refused(self, trip_id, driver_id):
        query = "UPDATE trip_table " \
                f"SET driver_id_refused = driver_id_refused || {driver_id}::bigint " \
                f"WHERE trip_id = '{trip_id}';"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def get_trip_status(self, trip_id):
        query = "SELECT status FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        trip_status_value = self.cursor.fetchall()[0][0]
        trip_status = Trip_status(trip_status_value)
        return trip_status

    @log_error_db
    def get_driver_id(self, trip_id):
        query = "SELECT driver_id FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        driver_id = self.cursor.fetchall()[0][0]
        return driver_id

    @log_error_db
    def get_driver_status(self, driver_id):
        query = "SELECT status FROM driver_table " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        driver_status_value = self.cursor.fetchall()[0][0]
        driver_status = Driver_status(driver_status_value)
        return driver_status

    @log_error_db
    def update_driver_status(self, driver_id, status):
        if type(status) != int:
            status = status.value
        query = "UPDATE driver_table " \
                f"SET status='{status}' " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        self.connection.commit()

    @log_error_db
    def get_driver_id_refused(self, trip_id):
        # return list of drivers who have rejected this trip
        query = "SELECT driver_id_refused FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        driver_id_refused = self.cursor.fetchall()[0][0]
        return driver_id_refused

    @log_error_db
    def get_driver_detail(self, driver_id):
        # return a list which is [driver_name,phone_number]
        query = "SELECT driver_name, phone_number FROM driver_table " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        driver_detail = self.cursor.fetchall()[0]
        return driver_detail

    @log_error_db
    def get_password_user(self, user_name):
        query = "SELECT password FROM user_table " \
                f"WHERE user_name = '{user_name}';"
        self.cursor.execute(query)
        password = self.cursor.fetchall()[0][0]
        return password

    @log_error_db
    def get_user_id(self, user_name):
        query = "SELECT user_id FROM user_table " \
                f"WHERE user_name = '{user_name}'"
        self.cursor.execute(query)
        user_id = self.cursor.fetchall()[0][0]
        return user_id
