from flask import Flask,make_response,url_for,request,render_template,session,redirect
from User import controler as controler
from User import config as config
import time


app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/',methods=['GET','POST'])
def index():
    user_logged_in,username = controler.check_user_status()
    if user_logged_in:
        if request.method == "POST":
            return redirect(url_for('booking'))
        return render_template('index.html',name=username)
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    user_logged_in, username = controler.check_user_status()
    if request.method == 'GET':
        if user_logged_in:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    elif request.method == "POST":
        return controler.set_cookie()

@app.route('/booking',methods=['GET','POST'])
def booking():
    user_logged_in, username = controler.check_user_status()
    if not user_logged_in:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            trip_id = request.cookies.get("trip_id", None)
            if trip_id == None:
                return render_template('booking.html')
            return render_template('show_booking_result.html',host=config.host,port=config.port,trip_id=trip_id)
        else:
            trip_id = controler.create_trip()
            resp = make_response(render_template('show_booking_result.html',host=config.host,port=config.port,trip_id=trip_id))
            resp.set_cookie('trip_id', trip_id)
            return resp

@app.route('/update_trip_status',methods=['GET','POST'])
def update_trip_status():
    time.sleep(1)
    trip_id = request.form["trip_id"]
    driver_id = controler.get_driver_id(trip_id)
    return driver_id


@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(host=config.host,port=config.port)
