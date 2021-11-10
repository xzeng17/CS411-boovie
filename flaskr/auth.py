from flask import Response

from . import sql

import jwt
import os
import hashlib
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
            sql.close(conn)
            return Response(str(e.args), status=500, mimetype='application/json')

        if existed_user:
            sql.close(conn)
            return Response({"User email already exists"}, status=403, mimetype='application/json')
        
        try:
            sql.reconnect(conn)
            sql.insert_string_values(conn, 'User', [email, md5_encode(password), role])
        except Exception as e:
            sql.close(conn)
            return Response(str(e.args), status=500, mimetype='application/json')
        sql.close(conn)
        return Response({"Registeration successful!"}, status=200, mimetype='application/json')


def login(conn, data_json):
    email       = data_json['Email']
    password    = md5_encode(data_json['Password'])
    
    existed_user = []

    try:
        #return read_table(conn, 'User')
        sql.reconnect(conn)
        existed_user = sql.get_user_by_email(conn, email)[0]
    except Exception as e:
        return Response({"Login failed."}, status=401, mimetype='application/json')
    
    if not existed_user or existed_user['user_password'] != password:
        return Response({"Login failed."}, status=401, mimetype='application/json')
    
    encoded = jwt.encode(existed_user, os.getenv('JWT_SECRET'), algorithm="HS256")

    resp = {
        "TOKEN": encoded,
        "ROLE": existed_user['role']
    }
    sql.close(conn)
    return Response(json.dumps(resp), status=200, mimetype='application/json')


def auth_login(conn, token)->bool:
    json_data = {}

    try:
        json_data = decode_token(token)
    except Exception as e:
        return False
    
    sql.reconnect(conn)
    existed_user = sql.get_user_by_email(conn, json_data["user_email"])[0]
    if not existed_user \
        or existed_user['user_password'] != json_data['user_password'] \
        or existed_user['role'] != json_data['role']:
        return False
    sql.close(conn)
    return True


def update_password(conn, user_email, new_password)->bool:
    sql.reconnect(conn)
    cursor = conn.cursor()
    stmt = "UPDATE USER\
            SET user_password = '{0}'\
            WHERE user_email='{1}';".format(md5_encode(new_password), user_email)
    cursor.execute(stmt)
    conn.commit()
    sql.close(conn)
    return True


def md5_encode(password:str)->str:
    result = hashlib.md5(password.encode())
    return result.hexdigest()


def decode_token(token)->dict:
    return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])