from threading import local
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import time
import creds
import locale


app = Flask(__name__)

app.secret_key = 'realhardik18iscool'
app.config['SESSION_COOKIE_NAME'] = 'realhardik18LovesCOOkies'
locale.setlocale(locale.LC_ALL, 'en_US')


@app.route('/home')
def home():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return render_template('index.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'])


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
    return render_template('stats.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'])


@app.route('/Stats/Artist/<time>')
def artists_stats(time):
    if time == 'four-weeks':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for item in sp.current_user_top_artists(limit=15, offset=0, time_range='short_term')['items']:
            local_dict = {}
            local_dict['name'] = item['name']
            local_dict['rank'] = str(rank)
            local_dict['followers'] = str(locale.format(
                "%d", int(item['followers']['total']), grouping=True))
            if len(item['genres']) == 0:
                local_dict['genres'] = ['Not Available']
            else:
                local_dict['genres'] = item['genres']
            local_dict['link_to_artist'] = item['external_urls']['spotify']
            local_dict['pfp_of_artist'] = item['images'][1]['url']
            local_dict['popularity_score'] = item['popularity']
            data.append(local_dict)
            rank += 1
        return render_template('topartists.html', user=sp.me()['display_name'], data=data, time_duration='four weeks')
    elif time == 'six-months':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for item in sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')['items']:
            local_dict = {}
            local_dict['name'] = item['name']
            local_dict['rank'] = str(locale.format(
                "%d", int(item['followers']['total']), grouping=True))
            local_dict['followers'] = item['followers']['total']
            if len(item['genres']) == 0:
                local_dict['genres'] = ['Not Available']
            else:
                local_dict['genres'] = item['genres']
            local_dict['link_to_artist'] = item['external_urls']['spotify']
            local_dict['pfp_of_artist'] = item['images'][1]['url']
            local_dict['popularity_score'] = item['popularity']
            data.append(local_dict)
            rank += 1
        return render_template('topartists.html', user=sp.me()['display_name'], data=data, time_duration='six months')
    elif time == 'lifetime':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for item in sp.current_user_top_artists(limit=20, offset=0, time_range='long_term')['items']:
            local_dict = {}
            local_dict['name'] = item['name']
            local_dict['rank'] = str(locale.format(
                "%d", int(item['followers']['total']), grouping=True))
            local_dict['followers'] = item['followers']['total']
            if len(item['genres']) == 0:
                local_dict['genres'] = ['Not Available']
            else:
                local_dict['genres'] = item['genres']
            local_dict['link_to_artist'] = item['external_urls']['spotify']
            local_dict['pfp_of_artist'] = item['images'][1]['url']
            local_dict['popularity_score'] = item['popularity']
            data.append(local_dict)
            rank += 1
        return render_template('topartists.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'], data=data, time_duration='a lifetime')
    else:
        return redirect(url_for('Stats'))


@app.route('/Stats/Tracks/<time>')
def tracks_stats(time):
    if time == 'four-weeks':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for track in sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')['items']:
            local_dict = dict()
            local_dict['url_to_artist'] = track['album']['artists'][0]['external_urls']['spotify']
            local_dict['name_of_artist'] = track['album']['artists'][0]['name']
            local_dict['name_of_track'] = track['name']
            local_dict['popularity'] = track['popularity']
            local_dict['rank'] = str(rank)
            local_dict['embed_url'] = f"https://open.spotify.com/embed/track/{track['id']}?utm_source=generator"
            if rank == 1:
                local_dict['color'] = '#ffd700'
            elif rank == 2:
                local_dict['color'] = '#C0C0C0'
            elif rank == 3:
                local_dict['color'] = '#CD7F32'
            else:
                local_dict['color'] = 'ffffff'
            local_dict['date_launched'] = track['album']['release_date']
            data.append(local_dict)
            rank += 1
        # return sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')['items'][0]['album']['release_date']
        return render_template('toptracks.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'], data=data, time_duration='four weeks')
    elif time == 'six-months':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for track in sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')['items']:
            local_dict = dict()
            local_dict['url_to_artist'] = track['album']['artists'][0]['external_urls']['spotify']
            local_dict['name_of_artist'] = track['album']['artists'][0]['name']
            local_dict['name_of_track'] = track['name']
            local_dict['popularity'] = track['popularity']
            local_dict['rank'] = str(rank)
            local_dict['embed_url'] = f"https://open.spotify.com/embed/track/{track['id']}?utm_source=generator"
            if rank == 1:
                local_dict['color'] = '#ffd700'
            elif rank == 2:
                local_dict['color'] = '#C0C0C0'
            elif rank == 3:
                local_dict['color'] = '#CD7F32'
            else:
                local_dict['color'] = 'ffffff'
            local_dict['date_launched'] = track['album']['release_date']
            data.append(local_dict)
            rank += 1
        # return sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')['items'][0]['album']['release_date']
        return render_template('toptracks.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'], data=data, time_duration='six months')
    elif time == 'lifetime':
        session['token_info'], authorized = get_token()
        session.modified = True
        if not authorized:
            return redirect('/')
        sp = spotipy.Spotify(auth=session.get(
            'token_info').get('access_token'))
        data = []
        rank = 1
        for track in sp.current_user_top_tracks(limit=20, offset=0, time_range='long_term')['items']:
            local_dict = dict()
            local_dict['url_to_artist'] = track['album']['artists'][0]['external_urls']['spotify']
            local_dict['name_of_artist'] = track['album']['artists'][0]['name']
            local_dict['name_of_track'] = track['name']
            local_dict['popularity'] = track['popularity']
            local_dict['rank'] = str(rank)
            local_dict['embed_url'] = f"https://open.spotify.com/embed/track/{track['id']}?utm_source=generator"
            if rank == 1:
                local_dict['color'] = '#ffd700'
            elif rank == 2:
                local_dict['color'] = '#C0C0C0'
            elif rank == 3:
                local_dict['color'] = '#CD7F32'
            else:
                local_dict['color'] = 'ffffff'
            local_dict['date_launched'] = track['album']['release_date']
            data.append(local_dict)
            rank += 1
        # return sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')['items'][0]['album']['release_date']
        return render_template('toptracks.html', user=sp.me()['display_name'], link_to_me=sp.me()['external_urls']['spotify'], data=data, time_duration='a lifetime')
    else:
        return redirect(url_for('Stats'))


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
        scope="user-top-read user-library-read user-read-email")


app.run(debug=True)
