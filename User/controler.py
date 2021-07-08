from flask import Flask,make_response,url_for,request,render_template,session,redirect
from Dispatch import view as dispatch_service

def check_user_status():
    try:
        username = request.cookies.get('username')
        if username in session:
            return True, username
        raise Exception("User is not logged in")
    except:
        return False,None

def set_cookie():
    if request.form['username'] not in session:
        session[request.form['username']] = True
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', request.form['username'])
        return resp
    return redirect(url_for('index'))

def create_trip():
    location_pickup = [request.form['lati_of_pickup'],request.form['long_of_pickup']]
    location_dropoff = [request.form['lati_of_dropoff'],request.form['long_of_dropoff']]
    user_name = request.cookies.get("username", None)
    trip_id = dispatch_service.create_trip(location_pickup,location_dropoff,user_name)
    return trip_id

def get_driver_id(trip_id):
    driver_id = dispatch_service.get_driver_id(trip_id)
    return driver_id
