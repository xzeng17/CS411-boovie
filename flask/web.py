from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
<<<<<<< HEAD
    return 'Hello, SauerkrautFishes!'

@app.route('/team')
def team():
    return {
        'Team_name:' : 'SauerkrautFish',
        'Team_members' : ['Xuankun Zeng', 'Jidong Huang', 'Yichuan Liu', 'Rodrigues Rohan'],
        'Project_name' : 'Boovie',
        'Wiki_URL' : 'https://wiki.illinois.edu/wiki/display/CS411AAFA21/Team+Sauerkraut+Fish+CS+411+Project+1'
    }
=======
    return 'Hello, SauerkrautFishes!!!'
>>>>>>> 1dff0df10f66cba9bf37444bddcee8827cd74f71
