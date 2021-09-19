from flaskext.mysql import MySQL
from flask import Response

def run(conn):
    try:
        # Begin create table Users
        cursor = conn.cursor()
        stmt = "DROP TABLE IF EXISTS Users;"
        cursor.execute(stmt)

        stmt = "CREATE TABLE Users (\
                FirstName VARCHAR(50) NOT NULL,\
                LastName VARCHAR(50) NOT NULL,\
                Email VARCHAR(255) PRIMARY KEY,\
                Password VARCHAR(50) NOT NULL,\
                Role VARCHAR(50) NOT NULL);"
        cursor.execute(stmt)
        
        stmt = "INSERT INTO Users \
                VALUE(%s, %s, %s, %s, %s);"
        vals = ('Xukun', 'Cai', 'xukuncai@gmail.com', 'icansing', 'manager')
        cursor.execute(stmt, vals)
        conn.commit()
        # End create table Users

    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    return Response(str("SQL init completed!"), status=200, mimetype='application/json')
