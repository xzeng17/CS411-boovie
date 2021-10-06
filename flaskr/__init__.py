from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import json

from . import sql
from . import sqlschema as schema

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
    if "Authorization" not in request.headers or \
        not sql.auth_login(sqlconn, request.headers["Authorization"][7:]):
        return Response({"Unauthorized user."}, status=401, mimetype='application/json')
    table_name = request.args.get('table')
    return sql.read_table(sqlconn, table_name)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data_json = json.loads(request.data)
        #print(data_json)
        return sql.register(sqlconn, data_json)
    
    return Response({"Bad request!"}, status=400, mimetype='application/json')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data_json = json.loads(request.data)
        #print(data_json)
        return sql.login(sqlconn, data_json)
    if request.method == 'GET':
        # authenticate user
        print(request.headers["Authorization"][7:])
        return sql.auth_login(sqlconn, request.headers["Authorization"][7:])
    return Response("Bad request!", status=400, mimetype='application/json')


# only perform once, comment out before deploy        
@app.route('/sqlschema')
def sqlschema():
    return schema.run(sqlconn)