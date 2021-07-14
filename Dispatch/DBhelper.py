from Dispatch import config
import psycopg2

class Helper:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                                      user=config.user_name,
                                      password=config.password,
                                      port=config.port,
                                      )
        self.cursor = self.connection.cursor()

    def insert_trip(self,trip_id,user_id,pickup_location,dropoff_location):
        pickup_location = "{" + f"{pickup_location[0]}" + "," + f"{pickup_location[1]}" + "}"
        dropoff_location = "{" + f"{dropoff_location[0]}" + "," + f"{dropoff_location[1]}" + "}"
        query = "INSERT INTO trip_table " \
                "(trip_id,user_id,status,pickup_location,dropoff_location)" \
                f"VALUES ('{trip_id}',{user_id},'created'," + "'" + f"{pickup_location}" + "'" + "," + "'" + f"{dropoff_location}" + "'" + ");"
        self.cursor.execute(query)
        self.connection.commit()

    def get_trip_detail(self,trip_id):
        query = "SELECT pickup_location,dropoff_location FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        self.connection.commit()
        res = self.cursor.fetchall()
        pickup_location = res[0][0]
        dropoff_location = res[0][1]
        return trip_id, pickup_location, dropoff_location

    def create_trip_table(self):
        # create_trip_table
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
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data_into_table(self):
        query = "COPY driver_table(driver_id,driver_name,status,phone_number,password,trip_id)" \
                "FROM 'driver_data.csv'" \
                "DELIMITER ','" \
                "CSV HEADER"
        self.cursor.execute(query)
        self.connection.commit()

    def create_driver_table(self):
        # create_driver_table
        query = "CREATE TABLE driver_table(" \
                "driver_id BIGSERIAL PRIMARY KEY," \
                "driver_name TEXT," \
                "status TEXT," \
                "phone_number VARCHAR(8)," \
                "password TEXT," \
                "trip_id TEXT);"
        self.cursor.execute(query)
        self.connection.commit()

    def update_trip_status(self,trip_id,driver_id,status):
        if status == "refused":
            query = "UPDATE trip_table " \
                    f"SET driver_id_refused = driver_id_refused || {driver_id}::bigint " \
                    f"WHERE trip_id = '{trip_id}';"
        else:
            query = "UPDATE trip_table " \
                    f"SET driver_id = {driver_id} ," \
                    f"status = '{status}' " \
                    f"WHERE trip_id = '{trip_id}';"
        self.cursor.execute(query)
        self.connection.commit()

    def get_trip_status(self,trip_id):
        query = "SELECT status FROM trip_table " \
                f"WHERE trip_id = {trip_id}"
        self.cursor.execute(query)
        trip_status = self.cursor.fetchall()[0][0]
        return trip_status

    def get_driver_id(self,trip_id):
        query = "SELECT driver_id FROM trip_table " \
                f"WHERE trip_id = {trip_id}"
        self.cursor.execute(query)
        driver_id = self.cursor.fetchall()[0][0]
        return driver_id

    def get_driver_status(self,driver_id):
        query = "SELECT status FROM driver_table " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        driver_status = self.cursor.fetchall()[0][0]
        return driver_status

    def update_driver_status(self,driver_id,status):
        query = "UPDATE driver_table " \
                f"SET status='{status}' " \
                f"WHERE driver_id = {driver_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def get_driver_id_refused(self,trip_id):
        # return list of drivers who have rejected this trip
        query = "SELECT driver_id_refused FROM trip_table " \
                f"WHERE trip_id = '{trip_id}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0][0]
        return result
