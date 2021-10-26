from .. import sql


def get_movie_history_by_email(conn, user_email)->list: # list of dict
    movies = []
    sql.reconnect(conn)
    try:
        cursor = conn.cursor()
        stmt = "SELECT * \
                FROM MovieHistory NATURAL JOIN Movie\
                WHERE user_email='{email}'".format(email=user_email)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]

        data = cursor.fetchall()
        for result in data:
            # result is a tuple (movie_id, user_email, title, language, img, video, date, rating, description)
            movies.append(dict(zip(row_headers,result)))
    except Exception as e:
        print(str(e.args))
    
    sql.close(conn)
    return movies
    # res =  json.dumps(json_data,indent=4, sort_keys=True, default=str)


def get_movie_details(conn, movie_id)->dict:
    movie = {}
    sql.reconnect(conn)
    try:
        cursor = conn.cursor()
        stmt = "SELECT * \
                FROM Movie\
                WHERE movie_id='{0}'".format(movie_id)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]

        data = cursor.fetchall()
        for result in data:
            # result is a tuple (movie_id, user_email, title, language, img, video, date, rating, description)
            movie = dict(zip(row_headers,result))
    except Exception as e:
        print(str(e.args))
    
    sql.close(conn)
    return movie