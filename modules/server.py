from bottle import route, run, request, get, post, template, response, redirect, static_file
import bottle
import elo, userhandle, os
from elo import make_list
from userhandle import create_account, get_lists

bottle.TEMPLATE_PATH.insert(0, '../views/')
datapath = "userdata/"

@route('/index')
def index():
    return

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

    return template('error', errortype=errortype, redirect_link=chosen_link)

@route('/signup')
def loadsignup():
    return template('signup')

@post('/signup')
def signup():
    username = request.forms.get("username")
    password = request.forms.get("password")
    cpassword = request.forms.get("cpassword")
    match create_account(username, password, cpassword):
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
    match userhandle.verify_credentials(username, password):
        case 'NOPATH': redirect('/error/' + "ACCOUNT_NONEXISTANT") 
        case 'INV_PASS': redirect('/error' + "INVALID_PASSWORD_L") 
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
        return template("all_lists", listz=None,user=None, signupplz="Please sign up or login to your account")

@post('/list')
def go_to_list():
    listname = request.forms.get('list')
    removelist= request.forms.get('remove_list')
    addlist=request.forms.get('add_list')
    if listname != None: 
        redirect('/list/' + listname)
        print(listname)
    if removelist != None: 
        redirect('/list/<listname>/clear') 
    if addlist != None: 
        redirect('/list/make_list')

@route('/list/make_list')
def show_ui():
    if request.get_cookie("user", secret='some-secret-key') != None: 
        return(template('makelist'))
    else: 
        return('Please login or signup to continue')
    
@post('/list/make_list')
def make_name():
    user=request.get_cookie("user", secret='some-secret-key') 
    if user!= None: 
        name=request.forms.get('name')
        makelist=make_list(user, name)
        print(name)
        if makelist=="SUCCESS":
            redirect('/list/' + name)
        elif makelist=="DUPATH": 
            return ("This path already exists")
        else: 
            return('idk what happened')
    else: 
        return('Please login or signup to continue')
    
    

@route('/list/<listname>')
def show_list(listname):
    if request.get_cookie("user", secret='some-secret-key') != None:
        user=request.get_cookie("user", secret='some-secret-key')
        data = elo.view_list(datapath + user + "/lists/" + listname + ".json")
        return template("list", data=data, listname=listname)
    else: 
        return('Please login or signup to continue')

@post('/list/<listname>/rank')
def rank_list(listname):
    action = request.forms.get('action')
    if request.get_cookie("user", secret='some-secret-key') != None:
        user=request.get_cookie("user", secret='some-secret-key')
        path = datapath + user + "/lists/" + listname + ".json"
        if action[:3] == "RNK":
            match elo.make_pairs(path):
                case 'NOPATH': redirect('/error/' + "FILE_PATH_ERROR")
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
        return('Please login or signup to continue')


@post('/list/<listname>/clear')
def del_list(listname):
    username = request.get_cookie("user", secret='some-secret-key')
    if os.remove(datapath + username + "/lists/" + listname + ".json"):
        redirect('/list')
    else:
        redirect('/error/' + "DEL_ERROR")

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
                case 'REDUN_ID': redirect('/error/' + "LIST_EXISTS") 
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
        return('Please login or signup to continue')

run(debug=True, reloader=True, port=8000)

