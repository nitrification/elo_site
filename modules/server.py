from bottle import route, run, request, get, post, template, response, redirect, static_file
import elo, userhandle, os, bottle

bottle.TEMPLATE_PATH.insert(0, '../views/')
datapath = "userdata/"

@route('/index')
def index():
    return

@route('/OH_SHIT')
def OH_SHIT():
    return "OH SHIT"

@route('/static/<filename>')
def styelsheet_static(filename):
    return static_file(filename, root="static/")

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

@route('/list')
def show_lists():
    username = 'testuser'
    pass

@route('/list/<listname>')
def show_list(listname):
    username = 'testuser'
    if username == 'testuser':
        data = elo.view_list(datapath + username + "/lists/" + listname + ".json")
        print(data, datapath)
        return template("list", data=data, listname=listname)
    else:
        return

@post('/list/<listname>/rank')
def rank_list(listname):
    action = request.forms.get('action')
    username = 'testuser'

    if username == 'testuser':
        path = datapath + username + "/lists/" + listname + ".json"
        if action[:3] == "RNK":
            match elo.make_pairs(path):
                case 'NOPATH': pass
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
                        case 'NOPATH': pass
                        case 'BUSY' : pass 
                        case 'SUCCESS': redirect('/list/' + listname)
                case 'SUCCESS':
                    pair = elo.get_pair(path)
                    if pair == 'NOPATH':
                        pass
                    else:
                        return template("comparison", pair=pair, listname=listname)


@post('/list/<listname>/clear')
def del_list(listname):
    username = 'testuser'
    if os.remove(datapath + username + "/lists/" + listname + ".json"):
        redirect('/list')
    else:
        redirect('/OH_SHIT')

@post('/list/<listname>')
def process_list(listname):
    action = request.forms.get('action')
    username = 'testuser'

    if username == 'testuser':
        path = datapath + username + "/lists/" + listname + ".json"
        if action[:3] == "ADD":
            match elo.add_item(path, request.forms.get('item')):
                case 'NOPATH': pass
                case 'BUSY': pass
                case 'SUCCESS':
                    match elo.sort_list(path):
                        case 'NOPATH': pass
                        case 'BUSY': pass
                        case 'REDUN_ID': pass
                        case 'SUCCESS': redirect('/list/' + listname)

        elif action[:3] == "DEL":
            item = action.split('_')[1]
            match elo.delete_item(path, item):
                case 'NOPATH': pass
                case 'BUSY': pass
                case 'SUCCESS':
                    match elo.sort_list(path):
                        case 'NOPATH': pass
                        case 'BUSY': pass
                        case 'SUCCESS': redirect('/list/' + listname)

run(debug=True, reloader=True, port=8000)
