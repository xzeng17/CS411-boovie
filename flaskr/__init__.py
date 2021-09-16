from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def hello():
    return 'Hello, SauerkrautFishes!'

@app.route('/team')
def team():
    return {
        'Team_name:' : 'SauerkrautFish',
        'Team_members' : ['Xuankun Zeng', 'Jidong Huang', 'Yichen Liu', 'Rodrigues Rohan'],
        'Project_name' : 'Boovie',
        'Wiki_URL' : 'https://wiki.illinois.edu/wiki/display/CS411AAFA21/Team+Sauerkraut+Fish+CS+411+Project+1'
    }
