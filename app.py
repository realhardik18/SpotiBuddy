from os import name
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = 'realhardik18isverycool'
app.config['SESSION_COOKIE_NAME'] = 'Realhardik18LovesCookies'


@app.route('/')
def index():
    return 'homepage'


@app.route('/tracks')
def tracks():
    return 'tracks of user'


app.run()
