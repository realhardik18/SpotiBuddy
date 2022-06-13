import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import time
import creds

app = Flask(__name__)

app.secret_key = 'realhardik18iscool'
app.config['SESSION_COOKIE_NAME'] = 'realhardik18LovesCOOkies'


@app.route('/home')
def home():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return render_template('index.html', user=sp.me()['display_name'])


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route('/redirect')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/home")


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/Stats')
def Stats():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return render_template('stats.html', user=sp.me()['display_name'])


@app.route('/Stats/Artist/four-weeks')
def artists_short_term():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    data = []
    rank = 1
    for item in sp.current_user_top_artists(limit=20, offset=0, time_range='short_term')['items']:
        local_dict = {}
        local_dict['name'] = item['name']
        local_dict['rank'] = str(rank)
        local_dict['monthly-listeners'] = item['followers']
        local_dict['genres'] = item['genres']
        local_dict['link_to_artist'] = item['href']
        local_dict['pfp_of_artist'] = item['images'][1]['url']
        data.append(local_dict)
        rank += 1
    return str(data)


@app.route('/Stats/Artist/six-months')
def artists_medium_term():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    data = []
    rank = 1
    for item in sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')['items']:
        local_dict = {}
        local_dict['name'] = item['name']
        local_dict['rank'] = str(rank)
        local_dict['monthly-listeners'] = item['followers']
        local_dict['genres'] = item['genres']
        local_dict['link_to_artist'] = item['href']
        local_dict['pfp_of_artist'] = item['images'][1]['url']
        data.append(local_dict)
        rank += 1
    return str(data)


@app.route('/Stats/Artist/lifetime')
def artists_long_term():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    data = []
    rank = 1
    for item in sp.current_user_top_artists(limit=20, offset=0, time_range='long_term')['items']:
        local_dict = {}
        local_dict['name'] = item['name']
        local_dict['rank'] = str(rank)
        local_dict['monthly-listeners'] = item['followers']
        local_dict['genres'] = item['genres']
        local_dict['link_to_artist'] = item['href']
        local_dict['pfp_of_artist'] = item['images'][1]['url']
        data.append(local_dict)
        rank += 1
    return str(data)


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60
    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(
            session.get('token_info').get('refresh_token'))
    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        redirect_uri=url_for('authorize', _external=True),
        scope="user-top-read user-library-read")


app.run(debug=True)
