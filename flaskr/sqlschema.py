from flaskext.mysql import MySQL
from flask import Response

def run(conn):

    cursor = conn.cursor()

    # drop all existing table
    try:
        stmt = "DROP TABLE IF EXISTS MovieHistory;"
        cursor.execute(stmt)
        stmt = "DROP TABLE IF EXISTS MovieReview;"
        cursor.execute(stmt)
        stmt = "DROP TABLE IF EXISTS Movie;"
        cursor.execute(stmt)

        stmt = "DROP TABLE IF EXISTS BookHistory;"
        cursor.execute(stmt)
        stmt = "DROP TABLE IF EXISTS BookReview;"
        cursor.execute(stmt)
        stmt = "DROP TABLE IF EXISTS Book;"
        cursor.execute(stmt)

        stmt = "DROP TABLE IF EXISTS User;"
        cursor.execute(stmt)
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table User
        stmt = "CREATE TABLE User (\
                    user_email		VARCHAR(50)     PRIMARY KEY NOT NULL,\
                    user_password	VARCHAR(50)     NOT NULL,\
                    role			VARCHAR(50)     \
                );"
        cursor.execute(stmt)
        
        stmt = "INSERT INTO User \
                VALUE(%s, %s, %s);"
        vals = ('xukuncai@gmail.com', 'icansing', 'manager')
        cursor.execute(stmt, vals)
        conn.commit()
        # End create table User
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table Movie
        stmt = "CREATE TABLE Movie (\
                    movie_id 		INT         PRIMARY KEY,\
                    title 			VARCHAR(50) NOT NULL,\
                    language		VARCHAR(50) NOT NULL,\
                    image_url		TEXT        NOT NULL,\
                    published_date	DATE        NOT NULL,\
                    rating			REAL,\
                    description		TEXT\
                );"
        cursor.execute(stmt)
        # End create table Movie
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table MovieReview
        stmt = "CREATE TABLE MovieReview (\
                    movie_review_id	INT	PRIMARY KEY,\
                    content		    TEXT	NOT NULL,\
                    movie_id 		INT,\
                    user_email		VARCHAR(50),\
                    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
                );"
        cursor.execute(stmt)
        # End create table MovieReview
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table MovieHistory
        stmt = "CREATE TABLE MovieHistory (\
                    user_email		VARCHAR(50) NOT NULL,\
                    movie_id 		INT NOT NULL,\
                    PRIMARY KEY (user_email, movie_id),\
                    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
                );"

        cursor.execute(stmt)
    # End create table MovieHistory
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')
    
    try:
        # Begin create table Book
        stmt = "CREATE TABLE Book (\
                    isbn		    INT PRIMARY KEY NOT NULL,\
                    title 			VARCHAR(50) NOT NULL,\
                    author  		VARCHAR(50) NOT NULL,\
                    language		VARCHAR(50) NOT NULL,\
                    image_url		TEXT        NOT NULL,\
                    published_date	DATE        NOT NULL,\
                    page_count		INT,\
                    description		TEXT,\
                    publisher		VARCHAR(50)\
                );"

        cursor.execute(stmt)
    # End create table Book
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table BookReview
        stmt = "CREATE TABLE BookReview (\
                    book_review_id	INT	PRIMARY KEY,\
                    content		TEXT	NOT NULL,\
                    isbn 			INT,\
                    user_email		VARCHAR(50),\
                    FOREIGN KEY (isbn) REFERENCES Book(isbn) ON DELETE CASCADE,\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
                );"
                
        cursor.execute(stmt)
    # End create table BookReview
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    try:
        # Begin create table BookHistory
        stmt = "CREATE TABLE BookHistory (\
                    user_email		VARCHAR(50) NOT NULL,\
                    book_id 		INT NOT NULL,\
                    PRIMARY KEY (user_email, book_id ),\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE,\
                    FOREIGN KEY (book_id ) REFERENCES Book(isbn) ON DELETE CASCADE \
                );"
                
        cursor.execute(stmt)
    # End create table BookHistory
    except Exception as e:
        return Response(str(e.args), status=400, mimetype='application/json')

    return Response(str("SQL init completed!"), status=200, mimetype='application/json')
