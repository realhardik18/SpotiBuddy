import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import time
import creds

app = Flask(__name__)

app.secret_key = 'realhardik18iscool'
app.config['SESSION_COOKIE_NAME'] = 'realhardik18LovesCOOkies'


@app.route('/')
def test():
    return 'test'
