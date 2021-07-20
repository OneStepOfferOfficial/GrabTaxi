from flask import app
import psycopg2

def log_error_db(f):
    def wrapper(*args):
        try:
            return f(*args)
        except IndexError:
            print(f'An IndexError was caught while using the api {f.__name__}')
        except psycopg2.OperationalError:
            print(f'A psycopg2 OperationalErrorr was caught while using the api {f.__name__}')
        except:
            print(f'A Common Error was caught while using the api {f.__name__}')
    return wrapper
d