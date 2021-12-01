from .. import sql


def get_book_histories_by_email(conn, user_email)->list: # list of dict
    stmt = "SELECT * \
            FROM BookHistory JOIN Book on (book_id = id)\
            WHERE user_email='{0}'".format(user_email)
    print("USER EMAIL IS>>>>>>>")
    print(stmt)
    return find_KV_pairs_with_stmt(conn, stmt)


def get_book_details(conn, book_id)->dict:
    stmt = "SELECT * \
            FROM Book\
             WHERE id='{0}'".format(book_id)
    print(stmt)
    return find_KV_pairs_with_stmt(conn, stmt)[0]


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

def has_book(conn, user_email, book_id)->bool:
    print("has book called")
    conn.ping()
    list_of_dict=[]
    try:
        cursor = conn.cursor()
        stmt = "SELECT * FROM BookHistory WHERE user_email = '{0}' AND book_id = '{1}'".format(user_email, book_id)
        cursor.execute(stmt)
        row_headers=[x[0] for x in cursor.description]
        data = cursor.fetchall()
        for result in data:
            list_of_dict.append(dict(zip(row_headers,result)))
    except Exception as e:
        print(str(e.args))
    sql.close(conn)
    return not not list_of_dict



def add_book(conn, user_email, book_id)->bool:
    print("Add called")
    conn.ping()
    try:
        sql.insert_values(conn, "BookHistory", [user_email, book_id])
    except Exception as e:
        print(str(e.args))
        return False
    sql.close(conn)
    return True


def delete_book(conn, user_email, book_id)->bool:
    print("Delete called")
    conn.ping()
    try:
        cursor = conn.cursor()
        stmt = "DELETE FROM BookHistory WHERE user_email = '{0}' AND book_id = '{1}'".format(user_email, book_id)
        cursor.execute(stmt)
        conn.commit()
    except Exception as e:
        print(str(e.args))
        return False
    sql.close(conn)
    return True