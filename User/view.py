from flask import Flask, make_response, url_for, request, render_template, session, redirect, jsonify
from User import controller as controller
from User import config as config
from flask_httpauth import HTTPBasicAuth
from Common.util import *
from Common.enum import *
from Common.decorator import *


app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', host=config.host, port=config.port)
    elif request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]
        return controller.login(user_name,password)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')
    else:
        token = request.form["token"]
        trip_id = controller.create_trip(token)
        if trip_id:
            return redirect(url_for('show_trip', trip_id=trip_id))
        return redirect(url_for('login'))

@app.route('/show_trip/<trip_id>', methods=['GET', 'POST'])
def show_trip(trip_id=None):
    return render_template('show_booking_result.html',trip_id=trip_id)

@app.route('/search_driver', methods=['GET', 'POST'])
@verify_token
def search_driver():
    trip_id = request.form["trip_id"]
    driver_id = controller.get_driver_id(trip_id)
    return str(driver_id)

@app.route('/get_driver_location', methods=['GET', 'POST'])
@verify_token
def get_driver_location():
    driver_id = request.form["driver_id"]
    driver_location = controller.get_driver_location(driver_id)
    longitude = float(driver_location[0])
    latitude = float(driver_location[1])
    position = {'longitude':longitude, 'latitude':latitude}
    return jsonify(position)

@app.route('/get_driver_detail',methods=['GET','POST'])
@verify_token
def get_driver_detail():
    driver_id = request.form["driver_id"]
    driver_detail = controller.get_driver_detail(driver_id)
    driver_name = driver_detail[0]
    phone_number = driver_detail[1]
    detail = {"driver_name":driver_name,"phone_number":phone_number}
    return jsonify(detail)

@app.route('/update_trip_status',methods=['GET','POST'])
@verify_token
def update_trip_status():
    trip_id = request.form["trip_id"]
    status = int(request.form["status"])
    controller.update_trip_status(trip_id,status)
    return "Done with updating trip status"

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    elif request.method == 'POST':
        name = request.form["name"]
        password = request.form['password']
        phone_number = request.form["phone_number"]
        character = request.form["character"]
        controller.sign_up(character,name,password,phone_number)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
