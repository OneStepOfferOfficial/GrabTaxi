from flask import Flask, make_response, url_for, request, render_template, session, redirect, jsonify
from User import controller as controller
from User import config as config
from Common.enum import *
import time

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/', methods=['GET', 'POST'])
def index():
    user_logged_in, username = controller.check_user_status()
    if user_logged_in:
        if request.method == "POST":
            return redirect(url_for('booking'))
        return render_template('index.html', name=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_logged_in, username = controller.check_user_status()
    if request.method == 'GET':
        if user_logged_in:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method == "POST":
        return controller.set_cookie()


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    user_logged_in, username = controller.check_user_status()
    if not user_logged_in:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            trip_id = request.cookies.get("trip_id", "0")
            if trip_id == "0":
                return render_template('booking.html')
            return render_template('show_booking_result.html', host=config.host, port=config.port, trip_id=trip_id)
        else:
            trip_id = controller.create_trip()
            resp = make_response(
                render_template('show_booking_result.html', host=config.host, port=config.port, trip_id=trip_id))
            resp.set_cookie('trip_id', trip_id)
            return resp


@app.route('/search_driver', methods=['GET', 'POST'])
def search_driver():
    time.sleep(1)
    trip_id = request.form["trip_id"]
    driver_id = controller.get_driver_id(trip_id)
    return str(driver_id)

@app.route('/get_driver_location', methods=['GET', 'POST'])
def get_driver_location():
    driver_id = request.form["driver_id"]
    driver_location = controller.get_driver_location(driver_id)
    longitude = float(driver_location[0])
    latitude = float(driver_location[1])
    position = {'longitude':longitude, 'latitude':latitude}
    return jsonify(position)

@app.route('/get_driver_detail',methods=['GET','POST'])
def get_driver_detail():
    driver_id = request.form["driver_id"]
    driver_detail = controller.get_driver_detail(driver_id)
    driver_name = driver_detail[0]
    phone_number = driver_detail[1]
    detail = {"driver_name":driver_name,"phone_number":phone_number}
    return jsonify(detail)

@app.route('/update_trip_status',methods=['GET','POST'])
def update_trip_status():
    trip_id = request.form["trip_id"]
    status = int(request.form["status"])
    controller.update_trip_status(trip_id,status)
    return "Done with updating trip status"

@app.route('/finished_my_trip')
def finished_my_trip():
    return controller.finished_my_trip()

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

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
