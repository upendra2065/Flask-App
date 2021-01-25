from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'

def connect_db():
    sql = sqlite3.connect(r'C:\Users\Upendra Kumar\Desktop\Eightfold AI\Flask App\Flask Basics\data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello, World!</h1>'

#Route Variables
@app.route('/home', methods=['GET', 'POST'], defaults={'name' : 'Defaults'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return render_template('home.html', name=name, display=False, mylist=['one', 'two', 'three', 'four'], listofdictionaries=[{'name' : 'Zach'}, {'name' : 'Zoe'}], results=results)
    # return '<h1>Hello {}, you are on the home page!</h1>'.format(name)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession'
    #Return jsonified version of Python Data Structure 
    return jsonify({'key' : 'value', 'listkey' : [1, 2, 3], 'name' : name})

#Request Query String
@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

#Request Form Data
@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        # return '''<form method="POST" action="/theform">
        #             <input type="text" name="name">
        #             <input type="text" name="location">
        #             <input type="submit" value="Submit">
        #         </form>'''
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        #return '<h1>Hello {}. You are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        #Redirects and url_for
        return redirect(url_for('home', name=name, location=location))

'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return '<h1>Hello {}. You are from {}. You have submitted the form successfully!</h1>'.format(name, location)
'''

#Request JSON Data
@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[0]['id'], results[0]['name'], results[0]['location'])

if __name__ == '__main__':
    app.run()