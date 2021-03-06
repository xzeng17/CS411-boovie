from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import json

from . import sql, managersql, auth
from . import sqlschema as schema
from .movie import moviequery
from .movie import moviedata
from .book import bookdata, bookquery

app = Flask(__name__)
CORS(app, supports_credentials=True)

load_dotenv()

sqlconn = sql.connect_MySQL(app)


@app.route('/')
def hello():
    return 'Hello, SauerkrautFishes!'

@app.route('/managebadges', methods=['PUT', 'DELETE'])
def manage_badges():
    if "Authorization" not in request.headers or \
        not auth.auth_login(sqlconn, request.headers["Authorization"][7:])\
        or 1 == 2:
        return Response({"Unauthorized user."}, status=401, mimetype='application/json')
    token = ""
    try:
        token = request.headers["Authorization"][7:]
    except Exception as e:
            return Response({"Unauthorized user."}, status=401, mimetype='application/json')
    user_info = auth.decode_token(token)

    if user_info["role"] != "manager":
        return Response({"Unauthorized user."}, status=401, mimetype='application/json')

    if request.method == 'PUT':
        managersql.update_badges(sqlconn)
        return Response({"Badges Updated"}, status=200, mimetype='application/json')

    if request.method == 'DELETE':
        managersql.delete_badges(sqlconn)
        return Response({"Badges deleted"}, status=200, mimetype='application/json')


@app.route('/team')
def team():
    return {
        'Team_name:' : 'SauerkrautFish',
        'Team_members' : ['Xuankun Zeng', 'Jidong Huang', 'Yichen Liu', 'Rodrigues Rohan'],
        'Project_name' : 'Boovie',
        'Wiki_URL' : 'https://wiki.illinois.edu/wiki/display/CS411AAFA21/Team+Sauerkraut+Fish+CS+411+Project+1',
        'ENV_VAR' : os.getenv('test')
    }


@app.route('/showtablecontent', methods=['GET'])
def showtablecontent():
    if "Authorization" not in request.headers or \
        not auth.auth_login(sqlconn, request.headers["Authorization"][7:]):
        return Response({"Unauthorized user."}, status=401, mimetype='application/json')
    table_name = request.args.get('table')
    return sql.read_table(sqlconn, table_name)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data_json = json.loads(request.data)
        #print(data_json)
        return auth.register(sqlconn, data_json)
    return Response({"Bad request!"}, status=400, mimetype='application/json')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data_json = json.loads(request.data)
        #print(data_json)
        return auth.login(sqlconn, data_json)
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Login failed"}, status=401, mimetype='application/json')
        
        if auth.auth_login(sqlconn, token):
            print(token)
            return Response({"User verified!"}, status=200, mimetype='application/json')
        return Response({"Login failed"}, status=401, mimetype='application/json')


# only perform once, comment out before deploy        
@app.route('/sqlschema')
def sqlschema():
    return schema.run(sqlconn)


# only perform once, comment out before deploy  
# @app.route('/initmovie')
# def initmovie():
#     return moviedata.init(sqlconn)


# test function only
@app.route('/test')
def test():
    sql.reconnect(sqlconn)
    # return str(moviedata.get_movie_review())
    # return str(moviedata.get_movie_review()[0]["author_details"]["username"])
    return str(moviedata.select_all_movie_id(sqlconn))


@app.route('/reconnectdb')
def reconnect():
    sqlconn.ping()
    return "Reconnection performed"


@app.route('/closedb')
def closedb():
    sqlconn.close()
    return "Connection closed"


@app.route('/book/history', methods=['GET'])
def get_book_history():
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Not authorized."}, status=401, mimetype='application/json')

        if not auth.auth_login(sqlconn, token):
            return Response({"Not authorized."}, status=401, mimetype='application/json')
        # end of authentication

        user_info = auth.decode_token(token)

        data = json.dumps(bookquery.get_book_histories_by_email(sqlconn, user_info["user_email"]), indent=4, sort_keys=True, default=str)
        return Response(data, status=200, mimetype='application/json')

@app.route('/user/badge', methods = ['GET'])
def get_user_badge():
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Not authorized."}, status=401, mimetype='application/json')

        if not auth.auth_login(sqlconn, token):
            return Response({"Not authorized."}, status=401, mimetype='application/json')
        # end of authentication

        user_info = auth.decode_token(token)

        data = json.dumps(moviequery.get_user_bages(sqlconn, user_info["user_email"]), indent=4, sort_keys=True, default=str)
        return Response(data, status=200, mimetype='application/json')

@app.route('/movie/history', methods=['GET'])
def get_movie_history():
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Not authorized."}, status=401, mimetype='application/json')

        if not auth.auth_login(sqlconn, token):
            return Response({"Not authorized."}, status=401, mimetype='application/json')
        # end of authentication

        user_info = auth.decode_token(token)

        data = json.dumps(moviequery.get_movie_histories_by_email(sqlconn, user_info["user_email"]), indent=4, sort_keys=True, default=str)
        return Response(data, status=200, mimetype='application/json')


@app.route('/book/details', methods=['GET'])
def get_book_details():
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Not authorized."}, status=401, mimetype='application/json')

        if not auth.auth_login(sqlconn, token):
            return Response({"Not authorized."}, status=401, mimetype='application/json')
        # end of authentication
    data = json.dumps(bookquery.get_book_details(sqlconn, request.args.get('book_id')), indent=4, sort_keys=True, default=str)
    print("data: ", data)
    return Response(data, status=200, mimetype='application/json')

@app.route('/movie/details', methods=['GET'])
def get_movie_details():
    if request.method == 'GET':
        # authenticate user
        token = ""
        try:
            token = request.headers["Authorization"][7:]
        except Exception as e:
            return Response({"Not authorized."}, status=401, mimetype='application/json')

        if not auth.auth_login(sqlconn, token):
            return Response({"Not authorized."}, status=401, mimetype='application/json')
        # end of authentication
    data = json.dumps(moviequery.get_movie_details(sqlconn, request.args.get('movie_id')), indent=4, sort_keys=True, default=str)
    print("data: ", data)
    return Response(data, status=200, mimetype='application/json')


@app.route('/movie/topusers')
def top_users():
    data = {
        "top_3_rating": moviequery.top_3_user_watching_3point_movie(sqlconn), 
        "top_3_rating_recent": moviequery.top_3_user_watching_recent_3point_movie(sqlconn)
        }
    return Response(json.dumps(data, indent=4, sort_keys=True, default=str), status=200, mimetype='application/json')


@app.route('/insertbooks')
def insertbooks():
    return bookdata.init(sqlconn)

@app.route('/import')
def import_data():
    bookdata.init(sqlconn)
    # bookreview.init(sqlconn)
    return moviedata.init(sqlconn)


@app.route('/searchbooks', methods=['GET', 'POST'])
def searchbooks():
    query = request.args.get('query')
    return sql.search_movies(sqlconn, query)


@app.route('/getmovies', methods=['GET'])
def getmovies():
    return sql.getmovies(sqlconn)

@app.route('/book/changeHistory', methods=['GET', 'POST', 'DELETE'])
def bookHistory():
    # authenticate user
    token = ""
    try:
        token = request.headers["Authorization"][7:]
    except Exception as e:
        return Response({"Not authorized."}, status=401, mimetype='application/json')

    if not auth.auth_login(sqlconn, token):
        return Response({"Not authorized."}, status=401, mimetype='application/json')
    # end of authentication
    
    user_info = auth.decode_token(token)
    user_email = user_info["user_email"]

    if request.method == 'GET':
        id = request.args.get('book_id')
        if bookquery.has_book(sqlconn, user_email, id):
            return Response("Success", status=200, mimetype='application/json')

    if request.method == 'POST':
        data_json = json.loads(request.data)
        print("HEHEHEHEHEHE")
        print(data_json)
        if bookquery.add_book(sqlconn, user_email, data_json['book_id']):
            return Response("Success", status=200, mimetype='application/json')

    if request.method == 'DELETE':
        data_json = json.loads(request.data)
        if bookquery.delete_book(sqlconn, user_email, data_json['book_id']):
            return Response("Success", status=200, mimetype='application/json')
    return Response({"Bad request."}, status=400, mimetype='application/json')






@app.route('/movie/changeHistory', methods=['GET', 'POST', 'DELETE'])
def movieHistory():
    # authenticate user
    token = ""
    try:
        token = request.headers["Authorization"][7:]
    except Exception as e:
        return Response({"Not authorized."}, status=401, mimetype='application/json')

    if not auth.auth_login(sqlconn, token):
        return Response({"Not authorized."}, status=401, mimetype='application/json')
    # end of authentication
    
    user_info = auth.decode_token(token)
    user_email = user_info["user_email"]

    if request.method == 'GET':
        movie_id = request.args.get('movie_id')
        if moviequery.has_movie(sqlconn, user_email, movie_id):
            return Response("Success", status=200, mimetype='application/json')

    if request.method == 'POST':
        data_json = json.loads(request.data)
        if moviequery.add_movie(sqlconn, user_email, data_json['movie_id']):
            return Response("Success", status=200, mimetype='application/json')

    if request.method == 'DELETE':
        data_json = json.loads(request.data)
        if moviequery.delete_movie(sqlconn, user_email, data_json['movie_id']):
            return Response("Success", status=200, mimetype='application/json')
    return Response({"Bad request."}, status=400, mimetype='application/json')


@app.route('/passwordchange', methods=['POST'])
def change_password():
    # authenticate user
    token = ""
    try:
        token = request.headers["Authorization"][7:]
    except Exception as e:
        return Response({"Not authorized."}, status=401, mimetype='application/json')

    if not auth.auth_login(sqlconn, token):
        return Response({"Not authorized."}, status=401, mimetype='application/json')
    # end of authentication
    print("token authenticated")
    if request.method == 'POST':
        user_info = auth.decode_token(token)
        user_email = user_info["user_email"]
        data_json = json.loads(request.data)
        old_password = auth.md5_encode(data_json["old_password"])
        if old_password == user_info["user_password"]:
            new_password = data_json["new_password"]
            auth.update_password(sqlconn, user_email, new_password)
            return Response("Success", status=200, mimetype='application/json')
    return Response({"Not authorized."}, status=401, mimetype='application/json')

@app.route('/deletemoviereview', methods=['POST', 'GET'])
def deletemoviereview():

    data_json = json.loads(request.data)
    movie_id = data_json.get('movie_id')
    print(movie_id)
    token = ""
    try:
        token = request.headers["Authorization"][7:]
        print(token)
    except Exception as e:
        return Response({"Not authorized."}, status=401, mimetype='application/json')

    if not auth.auth_login(sqlconn, token):
        return Response({"Not authorized."}, status=401, mimetype='application/json')

    user_info = auth.decode_token(token)
    user_email = user_info["user_email"]

    #print(user_email)
    sql.delete_row(sqlconn, movie_id, user_email)
    return "Worked"
# @app.route('/insertbookreviews')
# def insertbookreviews():
#     return bookreview.init(sqlconn)
