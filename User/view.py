from flask import Flask,make_response,url_for,request,render_template,session,redirect
from User import controller as controller
from User import config as config
import time


app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/',methods=['GET','POST'])
def index():
    user_logged_in,username = controller.check_user_status()
    if user_logged_in:
        if request.method == "POST":
            return redirect(url_for('booking'))
        return render_template('index.html',name=username)
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    user_logged_in, username = controller.check_user_status()
    if request.method == 'GET':
        if user_logged_in:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method == "POST":
        return controller.set_cookie()

@app.route('/booking',methods=['GET','POST'])
def booking():
    user_logged_in, username = controller.check_user_status()
    if not user_logged_in:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            trip_id = request.cookies.get("trip_id", None)
            if trip_id == None:
                return render_template('booking.html')
            return render_template('show_booking_result.html',host=config.host,port=config.port,trip_id=trip_id)
        else:
            trip_id = controller.create_trip()
            resp = make_response(render_template('show_booking_result.html',host=config.host,port=config.port,trip_id=trip_id))
            resp.set_cookie('trip_id', trip_id)
            return resp

@app.route('/search_driver',methods=['GET','POST'])
def search_driver():
    time.sleep(1)
    trip_id = request.form["trip_id"]
    driver_id = controller.get_driver_id(trip_id)
    return str(driver_id)

@app.route('/update_driver_location',methods=['GET','POST'])
def update_driver_location():
    driver_id = request.form["driver_id"]
    driver_location = controller.get_driver_location(driver_id)
    longitude = driver_location[0]
    latitude = driver_location[1]
    return  longitude,latitude

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(host=config.host,port=config.port)
