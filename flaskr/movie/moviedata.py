from logging import raiseExceptions

from .. import sql
from .. import auth

import requests
import os
import random
import uuid
import re


def check(test_str):
    #http://docs.python.org/library/re.html
    #re.search returns None if no position in the string matches the pattern
    #pattern to search for any character other then . a-z 0-9
    pattern = r'[^\.a-z0-9]'
    if re.search(pattern, test_str):
        return False
    else:
        return True


def get_top_rated_movies(page_number = 1)->list:# list of dict
    end_point = "movie/top_rated"+"?"+"api_key="
    api_url = os.getenv('MOVIE_API_BASE_URL')+end_point+os.getenv('MOVIE_API_KEY')\
        +"&language=en-US"+"&page="+str(page_number)

    response = requests.get(api_url)
    response_json = response.json()
    if "results" not in response_json or not response_json["results"]:
        raise Exception("Fail to fetch movies from API")
    return response_json["results"]


def top_rated_movies(number_needed: int = 1100)->dict:
    number_read:int = 0
    page_number:int = 1

    while number_read<number_needed:
        response:list = None
        try:
            response = get_top_rated_movies(page_number)
        except Exception as e:
            print(str(e.args))
            return

        for movie in response: # movie is dict
            if number_read == number_needed:
                return
            number_read+=1
            yield movie

        page_number += 1


def get_movie_review(movie_id:str = '19404', page_number:int = 1)->list:
    print("getting movie review")
    end_point = "movie/" + movie_id + "/reviews?api_key="
    api_url = os.getenv('MOVIE_API_BASE_URL')+end_point+os.getenv('MOVIE_API_KEY')\
        +"&language=en-US"+"&page="+str(page_number)
    
    response = requests.get(api_url)
    response_json = response.json()
    if "results" not in response_json or not response_json["results"]:
        raise Exception("Fail to fetch movies reviews from API")
    return response_json["results"]


def movie_reviews(movie_id:str)->dict:
    number_needed:int = random.randint(2,10) # randomly pick at most 2-10 reviews for each movie
    number_read:int = 0
    page_number:int = 0
    
    while number_read < number_needed:
        reviews:list = None
        page_number += 1
        try:
            reviews:list = get_movie_review(movie_id, page_number)
        except Exception as e:
            print(str(e))
            return
        
        for review in reviews:
            if number_read >= number_needed:
                return
            number_read += 1
            print("yielding review")
            yield review
    return


def get_video_url(movie_id:str)->str:
    end_point = "movie/{}/videos?api_key={}".format(movie_id, os.getenv('MOVIE_API_KEY'))
    url = os.getenv('MOVIE_API_BASE_URL')+end_point
    response = requests.get(url)
    response_json:dict = response.json()
    result:dict = response_json["results"][0]
    if result["site"] != "YouTube":
        return "N/A"
    return result["key"]


# ensure at least 1037 movies added to the database
# Only 376 reviews and 146 users are created
# therefore create 900 dummy users, 900 reviews and histories in the end
def init(conn):
    movie_inserted = 0
    review_inserted = 0

    for movie in top_rated_movies():
        # If want to add video, use movie id to get video key from another api
        video_url = "N/A"
        try:
            video_url = get_video_url(movie['id'])
        except Exception as e:
            print(str(e), "Cannot insert movie video url!")

        values = []
        try:
            values.append(movie['id'])
            values.append(movie['title'])
            values.append(movie['original_language'])
            values.append(movie['poster_path'])
            values.append(video_url)
            values.append(movie['release_date'])
            values.append(movie['vote_average'])
            values.append(movie['overview'])
        except Exception as e:
            print("############### <------ Fail To Extract Movie Info ------>###############")
            continue

        try:
            movie_inserted += 1
            sql.insert_values(conn, "Movie", values)
        except Exception as e:
            print("############### <------ Fail To Insert Movie ------>###############")
            print(str(e))
            movie_inserted -= 1
            continue
    
        for review in movie_reviews(str(movie['id'])):
            username = review["author_details"]["username"]
            if not check(username): continue
            email = username+"@gmail.com"
            password = os.getenv('DEFAULT_FAKE_USER_PW')

            if not sql.get_user_by_email(conn, email):
                sql.insert_values(conn, "User", [email, auth.md5_encode(password), "user"])

            #review_id = str(uuid.uuid4())
            review_id = review_inserted # Need to change back
            content = review["content"]

            values = [
                review_id,
                content,
                movie['id'],
                email
            ]

            try:
                review_inserted += 1
                sql.insert_values(conn, "MovieReview", values)
                values = [
                    email,
                    movie['id']
                ]
                sql.insert_values(conn, "MovieHistory", values)
            except Exception as e:
                review_inserted -= 1
                print(str(e))
                print("Failed to insert a MovieReview or MovieHistory")
        
    insert_fake_users(conn, review_inserted)

    return "Totally " + str(movie_inserted) + " real movies inserted to the database \n"\
        + "and " + str(review_inserted) + " real movie reviews inserted to the database."


def insert_fake_user(conn, user_id):
    email = user_id+"@fakemail.com"
    password = os.getenv('DEFAULT_FAKE_USER_PW')
    sql.insert_values(conn, "User", [email, auth.md5_encode(password), "user"])
    print("a fake user %s has been inserted", email)


def insert_fake_users(conn, review_id, number:int = 900):
    all_movie_ids:list = select_all_movie_id(conn)

    for i in range(1, number+1):
        user_id = "DummyUserNumber"+str(i)
        insert_fake_user(conn, user_id)
        insert_fake_review_history(
            conn,
            user_id, 
            all_movie_ids[random.randint(0, len(all_movie_ids)-1)],
            str(review_id+i)
            )


def insert_fake_review_history(conn, user_id, movie_id, review_id):
    email = user_id+"@fakemail.com"

    values = [
                review_id,
                "This is a really nice movie. -- by bot",
                movie_id,
                email
            ]
    sql.insert_values(conn, "MovieReview", values)

    values = [
                email,
                movie_id
            ]
    sql.insert_values(conn, "MovieHistory", values)
    print("fake review %d has been inserted", review_id)


def select_all_movie_id(conn)-> list:
    json_data = []

    try:
        cursor = conn.cursor()
        stmt = "SELECT movie_id FROM Movie"
        cursor.execute(stmt)
        data = cursor.fetchall()
        for result in data:
            json_data.append(result[0])

    except Exception as e:
        print("Cannot fetch movie_ids", str(e))
        return json_data

    return json_data