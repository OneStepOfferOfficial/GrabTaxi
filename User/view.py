from flask import Flask,make_response,url_for,request,render_template,session,redirect
import controler as controler
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
            return render_template('show_booking_result.html',trip_id=trip_id)
        else:
            print(1)
            trip_id = controler.create_trip()
            resp = make_response(render_template('show_booking_result.html',trip_id=trip_id))
            resp.set_cookie('trip_id', trip_id)
            return resp

@app.route('/update_trip_status',methods=['GET','POST'])
def update_trip_status():
    time.sleep(1)
    print("I am being called")

    return "1"


@app.route('/clear_session')

def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(port=5002, debug=True)

