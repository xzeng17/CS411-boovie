from flask import Response
from flaskext.mysql import MySQL

import jwt
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
            existed_user = json.loads(get_user_by_email(conn, email))
        except Exception as e:
            return Response(str(e.args), status=400, mimetype='application/json')

        if existed_user:
            return Response({"User email already exists"}, status=400, mimetype='application/json')
        
        try:
            insert_values(conn, 'Users', [first_name, last_tname, email, password, role])
        except Exception as e:
            return Response(str(e.args), status=400, mimetype='application/json')

        return Response({"Registeration successful!"}, status=200, mimetype='application/json')
        

def insert_values(conn, table_name: str, values: list):
    cursor = conn.cursor()
    stmt = "INSERT INTO {0} VALUES (%s);".format(table_name)
    cursor.execute(stmt%(", ").join(["\'"+x+"\'" for x in values]))
    conn.commit()


def delete_row(conn, table_name: str, values):
    cursor = conn.cursor()
    # need implementation


def login(conn, data_json):
    email       = data_json['Email']
    password    = data_json['Password']
    existed_user = []
    try:
        #return read_table(conn, 'Users')
        existed_user = json.loads(get_user_by_email(conn, email))[0]
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    if not existed_user or existed_user['Password'] != password:
        return Response({"Login failed."}, status=400, mimetype='application/json')
    
    encoded = jwt.encode(existed_user, os.getenv('JWT_SECRET'), algorithm="HS256")
    print(encoded)
    return Response(encoded, status=200, mimetype='application/json')


def auth_login(conn, token)->bool:
    json_data = {}
    try:
        json_data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
    except Exception as e:
        return False, Response({"Auth failed."}, status=401, mimetype='application/json')

    existed_user = json.loads(get_user_by_email(conn, json_data["Email"]))[0]
    if not existed_user \
        or existed_user['Password'] != json_data['Password'] \
        or existed_user['FirstName'] != json_data['FirstName'] \
        or existed_user['LastName'] != json_data['LastName'] \
        or existed_user['Role'] != json_data['Role']:
        return False, Response("Login failed", status=401, mimetype='application/json')

    return True, Response({"User verified!"}, status=200, mimetype='application/json')