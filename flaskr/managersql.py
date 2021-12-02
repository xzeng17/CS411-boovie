from . import sql

def update_badges(conn):
    stmt = "CALL assignBadge;"
    sql.reconnect(conn)
    cursor = conn.cursor()
    cursor.execute(stmt)
    conn.commit()


def delete_badges(conn):
    stmt = "UPDATE User SET keeper_badge = 'N/A', classic_badge = 'N/A', fashion_badge = 'N/A';"
    sql.reconnect(conn)
    cursor = conn.cursor()
    cursor.execute(stmt)
    conn.commit()