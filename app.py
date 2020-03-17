from flask import Flask, jsonify, send_file, request
from flask_cors import CORS 
import sqlite3

app = Flask(__name__)
# enable the api to be accessed by frontend running on localhost
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1"}})

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# define what to do when the user navigates to "/"
# this serves a static html file. 
@app.route('/')
def index():
    return send_file("static/html/index.html")


# A HTTP RESTful API Route returning the full restaurants dictionary
@app.route('/api/restaurants/all',  methods=['GET'])
def api_restaurants_all():
    conn = sqlite3.connect('restaurants.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_restaurants = cur.execute('SELECT * FROM restaurants;').fetchall()
    
    return jsonify(all_restaurants)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# A HTTP RESTful API Route returning a list of names of restaurants

@app.route('/api/restaurants/names',  methods=['GET'])
def api_restaurants_names():
    
    db_connection = sqlite3.connect('restaurants.db')
    db_cursor = db_connection.cursor()

    query = """SELECT NAME from restaurants"""

    
    db_cursor.execute(query)
    list_restaurants = db_cursor.fetchall()

    db_connection.close()

    return jsonify(list_restaurants)




# Run this application if the file is executed, e.g. as "python3 backend.py" 
if __name__ == '__main__': 
    app.testing=True
    app.run()