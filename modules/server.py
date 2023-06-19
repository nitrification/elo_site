from bottle import route, run, request, get, post, template, response
import bottle
import elo, userhandle, os

bottle.TEMPLATE_PATH.insert(0, '../views/')
datapath = "userdata/"

@route('/index')
def index():
    return

@route('/login')
def login():
    return

@post('/login')
def process_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    match userhandle.verify_credentials(username, password):
        case 'NOPATH':
            pass
        case 'INV_PASS':
            pass
        case 'SUCCESS':
            response.set_cookie("user", username, secret='some-secret-key')
            pass

@route('/signup')
def signup():
    return

@route('/list/<listname>')
def table(listname):
    username = 'testuser'
    if username == 'testuser':
        data = elo.view_list(datapath + username + "/lists/" + listname + ".json")
        return template("list", data=data, listname=listname)
    else:
        return

run(debug=True, reloader=True, port=8000)
