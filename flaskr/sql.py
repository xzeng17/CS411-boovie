import json
from flask import Response
from flaskext.mysql import MySQL
import json
import os


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
        print(str(e.args))
        return None

    return None


def read_table(conn, table_name: str)->list: # json array
    json_data = []
    reconnect(conn)
    try:
        cursor = conn.cursor()
        stmt = "SELECT * FROM {table}".format(table = table_name)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]
        data = cursor.fetchall()
        for result in data:
            json_data.append(dict(zip(row_headers,result)))
    except Exception as e:
        print(str(e.args))
    return json_data
    # res =  json.dumps(json_data,indent=4, sort_keys=True, default=str)


def get_user_by_email(conn, input_email: str)->list:
    json_data = []
    reconnect(conn)
    cursor = conn.cursor()
    stmt = "SELECT * FROM User WHERE user_email = \"{email}\"".format(email = input_email)
    user_info = cursor.execute(stmt)

    cursor.execute(stmt)
    row_headers=[x[0] for x in cursor.description]
    user_info = cursor.fetchall()

    for result in user_info:
        json_data.append(dict(zip(row_headers,result)))
    print(json_data)
    return json_data
        
def search_books(conn, query: str):
    json_data=[]
    reconnect(conn)
    cursor = conn.cursor()
    query = "\"%" + query + "%\""
    cursor.execute("SELECT * from Book WHERE title LIKE " + query)
    row_headers=[x[0] for x in cursor.description]
    conn.commit()
    data = cursor.fetchall()
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

def search_movies(conn, query: str):
    json_data=[]
    reconnect(conn)
    cursor = conn.cursor()
    query = "\"%" + query + "%\""
    cursor.execute("SELECT * from movie WHERE title LIKE " + query)
    row_headers=[x[0] for x in cursor.description]
    conn.commit()
    data = cursor.fetchall()
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data, default=str)

def insert_string_values(conn, table_name: str, values: list):
    # values is a list of string where each string will be enclosed by ''
    # this function currently doesn't support mix type insertion
    reconnect(conn)
    cursor = conn.cursor()
    stmt = "INSERT INTO {0} VALUES (%s);".format(table_name)
    cursor.execute(stmt%(", ").join(["\'"+x+"\'" for x in values]))
    conn.commit()


def insert_values(conn, table_name:str, values:list)->None:
    # this function is an extended version of above function
    # support mix type insertion
    reconnect(conn)
    cursor = conn.cursor()
    stmt = "INSERT INTO {0} VALUES (%s);".format(table_name)

    for i in range(len(values)):
        value = values[i]
        if type(value) is str:
            value = "\""+value+"\""
        else:
            value = str(value)
        values[i] = value

    cursor.execute(stmt%(", ").join(values))
    conn.commit()

def delete_row(conn, table_name: str, values):
    cursor = conn.cursor()
    # need implementation


def count_number_of_rows(conn, table_name: str):
    reconnect(conn)
    cursor = conn.cursor()
    stmt = "SELECT COUNT(*) FROM {0};".format(table_name)
    return str(cursor.execute(stmt))


def reconnect(conn)->None:
    conn.ping()


def close(conn)->None:
    conn.close()