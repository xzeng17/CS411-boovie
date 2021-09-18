from flask import Response
import os
from flaskext.mysql import MySQL

def connect_MySQL(app):
    try:
        # if os.getenv('MYSQL_LOCAL_DB_USER'):
        #     mysql = MySQL()
        #     app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_LOCAL_DB_USER')
        #     app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_LOCAL_ROOT_PASSWORD')
        #     app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_LOCAL_DB_NAME')
        #     app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_LOCAL_DB_HOST')
        #     mysql.init_app(app)
        #     return mysql.connect()
        
        if os.getenv('MYSQL_GCP_DB_USER'):
            mysql = MySQL()
            app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_GCP_DB_USER')
            app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_GCP_ROOT_PASSWORD')
            app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_GCP_DB_NAME')
            app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_GCP_DB_HOST')
            mysql.init_app(app)
            return mysql.connect()

    except Exception as e:
        return str(e.args)

    return None


def read_table(conn, table_name: str):
    data = []
    try:
        cursor = conn.cursor()
        stmt = "SELECT * FROM {table}"
        cursor.execute(stmt.format(table = table_name))
        data = cursor.fetchone()
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    res = []
    for ele in data:
        res.append(ele)

    return (', ').join(res)


