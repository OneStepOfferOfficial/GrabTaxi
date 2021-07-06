from flask import Flask,make_response,url_for,request,render_template,session,redirect
import uuid
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
    trip_id = str(uuid.uuid1()).replace('-','')
    return trip_id