from flask import Response
from flaskext.mysql import MySQL

import os
import json


def connect_MySQL(app):
    try:
        if os.getenv('MYSQL_LOCAL_DB_USER'):
            mysql = MySQL()
            app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_LOCAL_DB_USER')
            app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_LOCAL_ROOT_PASSWORD')
            app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_LOCAL_DB_NAME')
            app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_LOCAL_DB_HOST')
            mysql.init_app(app)
            return mysql.connect()
        
        # if os.getenv('MYSQL_GCP_DB_USER'):
        #     mysql = MySQL()
        #     app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_GCP_DB_USER')
        #     app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_GCP_ROOT_PASSWORD')
        #     app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_GCP_DB_NAME')
        #     app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_GCP_DB_HOST')
        #     mysql.init_app(app)
        #     return mysql.connect()

    except Exception as e:
        return str(e.args)

    return None


def read_table(conn, table_name: str)->json:
    json_data = []

    try:
        cursor = conn.cursor()
        stmt = "SELECT * FROM {table}".format(table = table_name)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]
        data = cursor.fetchall()
        for result in data:
            json_data.append(dict(zip(row_headers,result)))

    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    return json.dumps(json_data)


def get_user_by_email(conn, input_email: str)->json:
    json_data = []

    cursor = conn.cursor()
    stmt = "SELECT * FROM Users WHERE Email = \"{email}\"".format(email = input_email)
    user_info = cursor.execute(stmt)

    cursor.execute(stmt)
    row_headers=[x[0] for x in cursor.description]
    user_info = cursor.fetchall()

    for result in user_info:
        json_data.append(dict(zip(row_headers,result)))

    return json.dumps(json_data)


def register(conn, data_json):
        first_name  = data_json['FirstName']
        last_tname  = data_json['LastName']
        email       = data_json['Email']
        password    = data_json['Password']
        role        = data_json['Role']
        existed_user = []

        try:
            #return read_table(conn, 'Users')
            existed_user = (get_user_by_email(conn, email))
        except Exception as e:
            return Response(str(e.args), status=400, mimetype='application/json')
        print(existed_user)

        if existed_user != "[]":
            return Response("User email already exists", status=400, mimetype='application/json')
        return Response("Not exists", status=200, mimetype='application/json')
        

def insert_user(conn, request_data):
    try:
        cursor = conn.cursor()
        stmt = "need query statement"
        cursor.execute(stmt.format(email = request_data))
        user = cursor.fetchone()
    except Exception as e:
        return Response("Fail to insert user to DB", status=400, mimetype='application/json')