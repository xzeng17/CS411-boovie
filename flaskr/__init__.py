from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
from flaskext.mysql import MySQL
from . import db


app = Flask(__name__)
CORS(app, supports_credentials=True)

load_dotenv()

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_LOCAL_DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_LOCAL_ROOT_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_LOCAL_DB_NAME')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_LOCAL_DB_HOST')
mysql.init_app(app)
conn = mysql.connect()


@app.route('/')
def hello():
    return 'Hello, SauerkrautFishes!'

@app.route('/team')
def team():
    return {
        'Team_name:' : 'SauerkrautFish',
        'Team_members' : ['Xuankun Zeng', 'Jidong Huang', 'Yichen Liu', 'Rodrigues Rohan'],
        'Project_name' : 'Boovie',
        'Wiki_URL' : 'https://wiki.illinois.edu/wiki/display/CS411AAFA21/Team+Sauerkraut+Fish+CS+411+Project+1'
    }

@app.route('/showtablecontent', methods=['GET'])
def showtablecontent():
    table_name = request.args.get('table')
    return db.read_from_table(conn, table_name)