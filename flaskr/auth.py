from flask import Response

from . import sql

import jwt
import os
import json


def register(conn, data_json):
        # first_name  = data_json['FirstName']
        # last_tname  = data_json['LastName']
        print(data_json)
        email       = data_json['Email']
        password    = data_json['Password']
        role        = data_json['Role']
        existed_user = []

        try:
            sql.reconnect(conn)
            existed_user = sql.get_user_by_email(conn, email)
        except Exception as e:
            return Response(str(e.args), status=400, mimetype='application/json')

        if existed_user:
            return Response({"User email already exists"}, status=400, mimetype='application/json')
        
        try:
            sql.reconnect(conn)
            sql.insert_string_values(conn, 'User', [email, password, role])
        except Exception as e:
            return Response(str(e.args), status=400, mimetype='application/json')
        
        return Response({"Registeration successful!"}, status=200, mimetype='application/json')


def login(conn, data_json):
    email       = data_json['Email']
    password    = data_json['Password']
    
    existed_user = []

    try:
        #return read_table(conn, 'Users')
        sql.reconnect(conn)
        existed_user = sql.get_user_by_email(conn, email)[0]
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    if not existed_user or existed_user['user_password'] != password:
        return Response({"Login failed."}, status=400, mimetype='application/json')
    
    encoded = jwt.encode(existed_user, os.getenv('JWT_SECRET'), algorithm="HS256")
    print(encoded)
    return Response(encoded, status=200, mimetype='application/json')


def auth_login(conn, token):
    json_data = {}
    try:
        json_data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
    except Exception as e:
        return Response({"Auth failed."}, status=401, mimetype='application/json')

    sql.reconnect(conn)
    existed_user = sql.get_user_by_email(conn, json_data["user_email"])[0]
    if not existed_user \
        or existed_user['user_password'] != json_data['user_password'] \
        or existed_user['role'] != json_data['role']:
        return Response("Login failed", status=401, mimetype='application/json')

    return Response({"User verified!"}, status=200, mimetype='application/json')