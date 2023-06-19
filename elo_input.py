from bottle import run, route, template, get, post, request

@route('/')
def page():
    return("<h1>what a login page </h1>")
@get('/table')
def about():
    return template("table")
        

@post('/table')
def tableprocess():
    item = request.forms.get('item')
    item_list=[char for char in item]   
    return template("table", item_list=item_list)
run(debug=True, reloader=True, port=8000)
