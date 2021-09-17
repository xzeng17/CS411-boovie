from flask import Response

def read_from_table(conn, table_name: str):
    data = ""
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


