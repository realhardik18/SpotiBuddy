from os import name
from flask import Flask, request, url_for, session, redirect
import creds
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = 'realhardik18isverycool'
app.config['SESSION_COOKIE_NAME'] = 'Realhardik18LovesCookies'


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/tracks')
def tracks():
    return 'tracks of user'


@app.route('/redirect')
def redirectToPage():
    return "redirect"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        redirect_uri=url_for('redirectToPage', _external=True),
        scope='user-library-read'
    )


app.run()
