from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/add/<ab>')
def add(ab):
    result = sum([int(x) for x in ab.split('+')])
    return template('<b>{{result}}</b>', result=result)

run(lost='localhost', port=8080)
