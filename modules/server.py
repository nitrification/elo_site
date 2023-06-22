from bottle import route, run, request, get, post, template, response, redirect, static_file
import bottle
import elo, userhandle

bottle.TEMPLATE_PATH.insert(0, '../views/')
datapath = "userdata/"

@route('/index')
def index():
    user = request.get_cookie("user", secret='some-secret-key')
    if user:
        redirect('/list')
    else:
        return template('index')

@route('/static/<filename>')
def styelsheet_static(filename):
    return static_file(filename, root="static/")

@route('/error/<errortype>')
def showerror(errortype):
    chosen_link = ""
    match errortype:
        case "ACCOUNT_EXISTS":
            chosen_link = '/signup'
        case "INVALID_PASSWORD":
            chosen_link = '/signup'
        case "INVALID_PASSWORD_L":
            chosen_link = '/login'
        case "ACCOUNT_NONEXISTANT":
            chosen_link = '/login'
        case "FILE_PATH_ERROR":
            chosen_link = '/list'
        case "DEL_ERROR":
            chosen_link = '/list'
        case "LIST_EXISTS":
            chosen_link = '/list'
        case "ITEM_EXISTS":
            chosen_link = '/list'
        case "ZERO_ELEMENTS":
            chosen_link = '/list'
        case "NO_USER":
            chosen_link = '/login'


    return template('error', errortype=errortype, redirect_link=chosen_link)

#LOGIN/SIGNUP

@route('/signup')
def loadsignup(): 
    if request.get_cookie("user", secret='some-secret-key') != None:
        redirect ('/list')
    else:
        return template('signup')

@post('/signup')
def signup():
    username = request.forms.get("username")
    password = request.forms.get("password")
    cpassword = request.forms.get("cpassword")
    match userhandle.create_account(username, password, cpassword):
        case "DUPATH": redirect('/error/' + "ACCOUNT_EXISTS") 
        case "INV_PASS": redirect('/error/' + "INVALID_PASSWORD") 
        case "SUCCESS":
            response.set_cookie("user", username, secret='some-secret-key')
            redirect('/list')

@route('/login')
def display_login():
    if request.get_cookie("user", secret='some-secret-key') != None:
        redirect ('/list')
    else: 
        return template('login')

@post('/login')
def process_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    match userhandle.verify_credentials(datapath + username, password):
        case 'NOPATH': redirect('/error/' + "ACCOUNT_NONEXISTANT") 
        case 'INV_PASS': redirect('/error/' + "INVALID_PASSWORD_L") 
        case 'SUCCESS':
            response.set_cookie("user", username, secret='some-secret-key')
            redirect('/list')

@route('/logout')
def logout():
    response.delete_cookie("user", secret='some-secret-key') 
    return template('logout')

#LIST MENU 

@route('/list')
def show_lists():
    user = request.get_cookie("user", secret='some-secret-key')
    if user: 
        data = userhandle.get_lists(datapath + user)    
        return template("all_lists", data=data, user=user)

    else: 
        redirect('/error/' + "NO_USER")

@post('/list')
def process_all_list():
    action = request.forms.get('action')
    username = request.get_cookie("user", secret='some-secret-key')
    if username:
        path = datapath + username + "/lists/"
        if action[:3] == "ADD":
            match elo.make_list(path + request.forms.get('item') + ".json", request.forms.get('item')):
                case 'BUSY': pass
                case 'DUPATH': redirect('/error/' + "LIST_EXISTS") 
                case 'SUCCESS':
                    redirect('/list')

        elif action[:3] == "DEL":
            match elo.delete_list(path + action.split('_')[1] + ".json"):
                case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR") 
                case 'BUSY': pass
                case 'SUCCESS':
                    redirect('/list')

        elif action[:3] == "RED":
            redirect('/list/' + action.split('_')[1])

    else: 
        redirect('/error/' + "NO_USER")

#INDIVIDUAL LISTS MENU

@route('/list/<listname>')
def show_list(listname):
    if request.get_cookie("user", secret='some-secret-key') != None:
        user= request.get_cookie("user", secret='some-secret-key')
        data = elo.view_list(datapath + user + "/lists/" + listname + ".json")
        return template("list", data=data, listname=listname)
    else: 
        redirect('/error/' + "NO_USER")

@post('/list/<listname>')
def process_list(listname):
    action = request.forms.get('action')
    username = request.get_cookie("user", secret='some-secret-key')
    if username != None:
        path = datapath + username + "/lists/" + listname + ".json"
        if action[:3] == "ADD":
            match elo.add_item(path, request.forms.get('item')):
                case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR") 
                case 'BUSY': pass
                case 'REDUN_ID': redirect('/error/' + "ITEM_EXISTS") 
                case 'SUCCESS':
                    match elo.sort_list(path):
                        case 'NOPATH': redirect('/error/'  + "FILE_PATH_ERROR")
                        case 'BUSY': pass
                        case 'SUCCESS': redirect('/list/' + listname)

        elif action[:3] == "DEL":
            item = action.split('_')[1]
            match elo.delete_item(path, item):
                case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR") 
                case 'BUSY': pass
                case 'SUCCESS':
                    match elo.sort_list(path):
                        case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR") 
                        case 'BUSY': pass
                        case 'SUCCESS': redirect('/list/' + listname)
    else: 
        redirect('/error/' + "NO_USER")

#RANKING SYSTEM

@post('/list/<listname>/rank')
def rank_list(listname):
    action = request.forms.get('action')
    if request.get_cookie("user", secret='some-secret-key') != None:
        user=request.get_cookie("user", secret='some-secret-key')
        path = datapath + user + "/lists/" + listname + ".json"
        if action[:3] == "RNK":
            match elo.make_pairs(path):
                case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR")
                case 'Z_INDEX' : redirect('/error/' + "ZERO_ELEMENTS")
                case 'BUSY': pass
                case 'SUCCESS':
                    pair = elo.get_pair(path)
                    if pair == 'NOPATH':
                        pass
                    else:
                        return template("comparison", pair=pair, listname=listname)

        elif action[:3] == "NXT":
            winner = int(action.split('_')[1])
            match elo.update_list(path, winner):
                case 'NOPATH': pass
                case 'END_OF_LIST': 
                    match elo.sort_list(path):
                        case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR") 
                        case 'BUSY' : pass 
                        case 'SUCCESS': redirect('/list/' + listname)
                case 'SUCCESS':
                    pair = elo.get_pair(path)
                    if pair == 'NOPATH':
                        redirect('/error/' + "FILE_PATH_ERROR")
                    else:
                        return template("comparison", pair=pair, listname=listname)
    else: 
        redirect('/error/' + "NO_USER")

def start():
    run(debug=True, reloader=True, port=8000)

if __name__ == "__main__":
    print("attempting to run module as main")
