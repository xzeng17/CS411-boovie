from .. import sql


def get_movie_histories_by_email(conn, user_email)->list: # list of dict
    stmt = "SELECT * \
            FROM MovieHistory NATURAL JOIN Movie\
            WHERE user_email='{0}'".format(user_email)
    return find_KV_pairs_with_stmt(conn, stmt)


def get_movie_details(conn, movie_id)->dict:
    stmt = "SELECT * \
            FROM Movie\
            WHERE movie_id='{0}'".format(movie_id)
    return find_KV_pairs_with_stmt(conn, stmt)[0]


# Find the top users who watches the most number of movies rated over 3 stars
def top_3_user_watching_3point_movie(conn):
    stmt = "SELECT user_email \
            FROM MovieHistory\
            WHERE movie_id IN (\
                SELECT movie_id\
                FROM Movie\
                WHERE rating >= 1\
            )\
            GROUP BY user_email\
            ORDER BY COUNT(user_email) DESC\
            LIMIT 3;"
    return find_single_attribute_with_stmt(conn, stmt)


# Find the top users who watches the most number of movies rated over 3 stars
# with published_date greater a certin date
# And the movie need to be reviewed.
def top_3_user_watching_recent_3point_movie(conn):
    stmt = "SELECT user_email\
            FROM MovieHistory \
            WHERE movie_id IN (\
                SELECT DISTINCT movie_id\
                FROM Movie NATURAL JOIN MovieReview\
                WHERE rating >= 8 and published_date >= '2020-01-01'\
            )\
            GROUP BY user_email\
            ORDER BY COUNT(user_email) DESC\
            LIMIT 3;"
    return find_single_attribute_with_stmt(conn, stmt)


# a generic function returns a list of single_attribute with stmt prepared from caller function
def find_single_attribute_with_stmt(conn, stmt)->list:#list of string
    list_of_string = []
    sql.reconnect(conn)
    try:
        cursor = conn.cursor()
        cursor.execute(stmt)
        data = cursor.fetchall()
        for result in data:
            list_of_string.append(result[0])
    except Exception as e:
        print(str(e.args))
    print(list_of_string)
    return list_of_string


def find_KV_pairs_with_stmt(conn, stmt)->list:#list of dict
    list_of_dict = []
    sql.reconnect(conn)
    try:
        cursor = conn.cursor()
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]
        data = cursor.fetchall()
        for result in data:
            list_of_dict.append(dict(zip(row_headers,result)))
    except Exception as e:
        print(str(e.args))
    sql.close(conn)
    return list_of_dict


def has_movie(conn, user_email, movie_id)->bool:
    print("has movie called")
    conn.ping()
    list_of_dict=[]
    try:
        cursor = conn.cursor()
        stmt = "SELECT * FROM MovieHistory WHERE user_email = '{0}' AND movie_id = '{1}'".format(user_email, movie_id)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]
        data = cursor.fetchall()
        for result in data:
            list_of_dict.append(dict(zip(row_headers,result)))
    except Exception as e:
        print(str(e.args))
    sql.close(conn)
    return not not list_of_dict


def add_movie(conn, user_email, movie_id)->bool:
    print("Add called")
    conn.ping()
    try:
        sql.insert_values(conn, "MovieHistory", [user_email, movie_id])
    except Exception as e:
        print(str(e.args))
        return False
    sql.close(conn)
    return True


def delete_movie(conn, user_email, movie_id)->bool:
    print("Delete called")
    conn.ping()
    try:
        cursor = conn.cursor()
        stmt = "DELETE FROM MovieHistory WHERE user_email = '{0}' AND movie_id = '{1}'".format(user_email, movie_id)
        cursor.execute(stmt)
        conn.commit()
    except Exception as e:
        print(str(e.args))
        return False
    sql.close(conn)
    return True