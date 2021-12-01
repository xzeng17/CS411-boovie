from flask import Response
from . import auth

def run(conn):
    conn.ping() # refresh connection
    cursor = conn.cursor()
    # drop all existing table and triggers

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
        stmt = "SET NAMES 'utf8mb4';"
        cursor.execute(stmt)

        stmt = "DROP TRIGGER IF EXISTS oldSchoolBadgeTrigger;"
        cursor.execute(stmt)
        stmt = "DROP TRIGGER IF EXISTS FashionBadgeTrigger;"
        cursor.execute(stmt)
        stmt = "DROP TRIGGER IF EXISTS keeperBadgeTrigger;"
        cursor.execute(stmt)
        stmt = "DROP TRIGGER IF EXISTS DeleteFashionBadgeTrigger;"
        cursor.execute(stmt)
        stmt = "DROP TRIGGER IF EXISTS DeleteKeeperBadgeTrigger;"
        cursor.execute(stmt)
        stmt = "DROP TRIGGER IF EXISTS DeleteClassicBadgeTrigger;"
        cursor.execute(stmt)

    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table User
        stmt = "CREATE TABLE User (\
                    user_email		VARCHAR(50)     PRIMARY KEY NOT NULL,\
                    user_password	VARCHAR(50)    NOT NULL,\
                    role			VARCHAR(50)    NOT NULL, \
                    classic_badge VARCHAR(50)    NOT NULL,\
                    fashion_badge VARCHAR(50) NOT NULL,\
                    keeper_badge VARCHAR(50) NOT NULL\
                );"
        cursor.execute(stmt)
        
        stmt = "INSERT INTO User \
                VALUE(%s, %s, %s, %s, %s, %s);"
        vals = ('xukuncai@gmail.com', auth.md5_encode('icansing'), 'manager', 'N/A', 'N/A', 'N/A')
        cursor.execute(stmt, vals)
        conn.commit()
        # End create table User
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table Movie
        # image_url: only poster_path included
        # video_url: only youtube key included
        stmt = "CREATE TABLE Movie (\
                    movie_id 		INT         PRIMARY KEY,\
                    title 			VARCHAR(50) NOT NULL,\
                    language		VARCHAR(50) NOT NULL,\
                    image_url		TEXT        NOT NULL,\
                    video_url       TEXT        NOT NULL,\
                    published_date	DATE        NOT NULL,\
                    rating			REAL,\
                    description		TEXT\
                );"
        cursor.execute(stmt)
        # End create table Movie
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table MovieReview
        stmt = "CREATE TABLE MovieReview (\
                    movie_review_id	VARCHAR(255)	PRIMARY KEY,\
                    content		    TEXT	        NOT NULL,\
                    movie_id 		INT,\
                    user_email		VARCHAR(50),\
                    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
                );"
        cursor.execute(stmt)
        # End create table MovieReview
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table MovieHistory
        stmt = "CREATE TABLE MovieHistory (\
                    user_email		VARCHAR(50) NOT NULL,\
                    movie_id 		INT         NOT NULL,\
                    PRIMARY KEY (user_email, movie_id),\
                    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
                );"

        cursor.execute(stmt)
    # End create table MovieHistory
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')
    
    try:
        # Begin create table Book
        stmt = "CREATE TABLE Book (\
                    id              VARCHAR(50) PRIMARY KEY NOT NULL,\
                    isbn		    VARCHAR(50),\
                    title 			TEXT NOT NULL,\
                    author  		TEXT NOT NULL,\
                    language		VARCHAR(50) NOT NULL,\
                    image_url		TEXT        NOT NULL,\
                    published_date	VARCHAR(50) NOT NULL,\
                    page_count		INT,\
                    description		TEXT,\
                    publisher		TEXT\
                );"

        cursor.execute(stmt)
    # End create table Book
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table BookReview
        stmt = "CREATE TABLE BookReview (\
                    book_review_id	VARCHAR(100)	PRIMARY KEY,\
                    content		TEXT	NOT NULL,\
                    id 			VARCHAR(50),\
                    user_email		VARCHAR(50)\
                );"
        # FOREIGN KEY (id) REFERENCES Book(id) ON DELETE CASCADE,\
        # FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE\
        cursor.execute(stmt)
    # End create table BookReview
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create table BookHistory
        stmt = "CREATE TABLE BookHistory (\
                    user_email		VARCHAR(50) NOT NULL,\
                    book_id 		VARCHAR(50) NOT NULL,\
                    PRIMARY KEY (user_email, book_id ),\
                    FOREIGN KEY (user_email) REFERENCES User(user_email) ON DELETE CASCADE,\
                    FOREIGN KEY (book_id ) REFERENCES Book(id) ON DELETE CASCADE \
                );"
                
        cursor.execute(stmt)
    # End create table BookHistory
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create classic badge trigger
        stmt = "create trigger oldSchoolBadgeTrigger after insert on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = new.user_email and m.published_date < 19700101);\
                    if @x > 3 then\
                        UPDATE USER set classic_badge = 'Yes' WHERE\
                        user_email = new.user_email;\
                    end if;\
                end;\
                "
        cursor.execute(stmt)
    # End create classic badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create fashion badge trigger
        stmt = "create trigger FashionBadgeTrigger after insert on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = new.user_email and m.published_date > 20100101);\
                    if @x > 3 then\
                        UPDATE USER set fashion_badge = 'Yes' WHERE\
                        user_email = new.user_email;\
                    end if;\
                end;\
                "
        cursor.execute(stmt)
    # End create fashion badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')


    try:
        # Begin create keeper badge trigger
        stmt = "create trigger keeperBadgeTrigger after insert on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = new.user_email);\
                    if @x > 10 then\
                        UPDATE USER set keeper_badge = 'Yes' WHERE\
                        user_email = new.user_email;\
                    end if;\
                end;\
                "
        cursor.execute(stmt)
    # End create keeper badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    try:
        # Begin create delete fashion badge trigger
        stmt = "create trigger DeleteFashionBadgeTrigger after delete on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = old.user_email and m.published_date > 20100101);\
                    if @x <= 3 then\
                        UPDATE USER set fashion_badge = 'N/A' WHERE\
                        user_email = old.user_email;\
                    end if;\
                end;\
                "
        cursor.execute(stmt)
    # End create fashion badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')


    # try:
    #     # Begin create fashion badge trigger
    #     stmt = "create trigger DeleteFashionBadgeTrigger2 after delete on MovieHistory\
    #             for each row\
    #             begin\
    #                 set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = old.user_email and m.published_date > 20100101);\
    #                 if @x > 3 then\
    #                     UPDATE USER set fashion_badge = 'Yes' WHERE\
    #                     user_email = old.user_email;\
    #                 else \
    #                     if @x <= 3 then\
    #                         UPDATE USER set fashion_badge = 'N/A' WHERE\
    #                         user_email = old.user_email;\
    #                     end if; \
    #                 end if;\
    #             end;\
    #             "
    #     cursor.execute(stmt)
    # # End create fashion badge trigger
    # except Exception as e:
    #     return Response(str(e.args), status=500, mimetype='application/json')


    try:
        # Begin create delete keeper badge trigger
        stmt = "create trigger DeleteKeeperBadgeTrigger after delete on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = old.user_email and m.published_date > 20100101);\
                    if @x <= 10 then\
                        UPDATE USER set keeper_badge = 'N/A' WHERE\
                        user_email = old.user_email;\
                    end if;\
                end;\
                "
        cursor.execute(stmt)

    # End create fashion badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')
    try:
        # Begin create Delete Classic Badge Trigger
        stmt = "create trigger DeleteClassicBadgeTrigger after delete on MovieHistory\
                for each row\
                begin\
                    set @x = (select count(movie_id) from MovieHistory natural join Movie m where user_email = old.user_email and m.published_date < 19700101);\
                    if @x <= 3 then\
                        UPDATE USER set classic_badge = 'N/A' WHERE\
                        user_email = old.user_email;\
                    end if; \
                end;\
                "
        cursor.execute(stmt)
    # End create fashion badge trigger
    except Exception as e:
        return Response(str(e.args), status=500, mimetype='application/json')

    # try:
        # stmt = "ALTER TABLE Movie CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;"
        # cursor.execute(stmt)
        # stmt = "ALTER TABLE Book CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;"
        # cursor.execute(stmt)
        # stmt = "ALTER TABLE User CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;"
        # cursor.execute(stmt)
        # stmt = "ALTER TABLE MovieReview CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;"
        # cursor.execute(stmt)
        # stmt = "ALTER TABLE BookReview CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;"
        # cursor.execute(stmt)
    # except Exception as e:
    #     return Response(str(e.args), status=400, mimetype='application/json')

    return Response("SQL init completed!", status=200, mimetype='application/json')
