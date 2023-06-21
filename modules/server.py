from bottle import route, run, request, get, post, template, response, redirect,cookie_decode
import bottle
import elo, userhandle, os
from userhandle import create_account, verify_credentials,get_lists

bottle.TEMPLATE_PATH.insert(0, '../views/')
datapath = "userdata/"

@route('/index')
def index():
    return
@route('/signup')
def loadsignup():
    return template('signup')
@post('/signup')
def signup():
    username = request.forms.get("username")
    password = request.forms.get("password")
    cpassword = request.forms.get("cpassword")
    print("hello")
    responses=create_account(username, password, cpassword)
    if responses == "DUPATH":
        return "<p>u did it</p>"
    if responses == "INV_PASS":
        return "<p>Your passwords did not match. Try again. </p>"
    if responses == "SUCCESS":
        response.set_cookie("user", username, secret='some-secret-key')
        return "<p>success</p>"

@route('/login')
def display_login():
    return template('login')
@post('/login')
def process_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    match userhandle.verify_credentials(username, password):
        case 'NOPATH':
            return("<p>user not found, please go sign up for an account or try again.")
        case 'INV_PASS':
            return("<p>password incorrect. please try again. </p>")
        case 'SUCCESS':
            response.set_cookie("user", username, secret='some-secret-key')
            redirect('/list')
   

@route('/list')
def show_lists():
    if request.get_cookie("user", secret='some-secret-key') != None:
        username=request.get_cookie("user", secret='some-secret-key')
        print(username)
        listz=get_lists(username)
        if listz!="NOPATH":
            return(template("all_lists", listz=listz, user=username, signupplz=""))
        else:
            return(template("all_lists",listz=None, user=username, signupplz=""))
    else:
        return template("all_lists", signupplz="<h1>Please sign up or login to your account </h1>")

@post('/list')
def go_to_list():
    listname = request.forms.get('')

@route('/list/<listname>')
def show_list(listname):
    username = 'testuser'
    if username == 'testuser':
        data = elo.view_list(datapath + username + "/lists/" + listname + ".json")
        return template("list", data=data, listname=listname)
    else:
        return

@post('/list/<listname>')
def process_list(listname):
    return
run(debug=True, reloader=True, port=8000)

