from flask import request
import psycopg2
from Common.util import *
from functools import wraps


def log_error_db(f):
    @wraps(f)
    def wrapper(self,*args,**kwargs):
        try:
            return f(self,*args,**kwargs)
        except IndexError:
            print(f'An IndexError was caught while using the api {f.__name__}')
        except psycopg2.OperationalError:
            print(f'A psycopg2 OperationalErrorr was caught while using the api {f.__name__}')
        except:
            print(f'A Common Error was caught while using the api {f.__name__}')
    return wrapper

def verify_token(f):
    @wraps(f)
    def helpper(*args):
        token = request.headers.get('token')
        token_data = verify_token_and_return_data(token)
        if token_data:
            return f(*args)
        else:
            return "expired"
    return helpper
