from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

from . import sql


app = Flask(__name__)
CORS(app, supports_credentials=True)

load_dotenv()

sqlconn = sql.connect_MySQL(app)

@app.route('/')
def hello():
    return 'Hello, SauerkrautFishes!'

@app.route('/team')
def team():
    return {
        'Team_name:' : 'SauerkrautFish',
        'Team_members' : ['Xuankun Zeng', 'Jidong Huang', 'Yichen Liu', 'Rodrigues Rohan'],
        'Project_name' : 'Boovie',
        'Wiki_URL' : 'https://wiki.illinois.edu/wiki/display/CS411AAFA21/Team+Sauerkraut+Fish+CS+411+Project+1',
        'ENV_VAR' : os.getenv('test')
    }

@app.route('/showtablecontent', methods=['GET'])
def showtablecontent():
    table_name = request.args.get('table')
    return sql.read_table(sqlconn, table_name)