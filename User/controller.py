from flask import Flask,make_response,url_for,request,render_template,session,redirect
from Dispatch import view as dispatch_service
from Common.enum import *

def check_user_status():
    try:
        user_id = request.cookies.get('user_id')
        if user_id in session:
            return True, request.cookies.get('user_name')
        raise Exception("User is not logged in")
    except :
        return False,None

def login(user_name,password):
    if dispatch_service.verify_password_user(user_name,password):
        user_id = dispatch_service.get_user_id(user_name)
        session[user_id] = True
        resp = make_response(redirect(url_for('booking')))
        resp.set_cookie('user_id',str(user_id))
        resp.set_cookie('user_name',user_name)
        return resp
    else:
        return redirect(url_for('login'))

def create_trip():
    location_pickup = [float(request.form['lati_of_pickup']),float(request.form['long_of_pickup'])]
    location_dropoff = [float(request.form['lati_of_dropoff']),float(request.form['long_of_dropoff'])]
    user_id = int(request.cookies.get("user_id", None))
    trip_id = dispatch_service.create_trip(location_pickup,location_dropoff,user_id)
    return trip_id

def get_driver_id(trip_id):
    driver_id = dispatch_service.get_driver_id(trip_id) 
    return driver_id

def get_driver_location(driver_id):
    driver_location = dispatch_service.get_driver_location(driver_id)
    return driver_location

def get_driver_detail(driver_id):
    driver_detail = dispatch_service.get_driver_detail(driver_id)
    return driver_detail

def update_trip_status(trip_id,status):
    status = Trip_status(status)
    dispatch_service.update_trip_status(trip_id,status)

def finished_my_trip():
    resp = make_response(
        redirect(url_for('index')))
    resp.set_cookie('trip_id', "0")
    return resp

def sign_up(character,name,password,phone_number):
    if character == "user":
        dispatch_service.sign_up_user(name,password,phone_number)
    elif character == "driver":
        dispatch_service.sign_up_driver(name,password,phone_number)
