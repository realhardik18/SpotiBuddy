from creds import client_id, client_secret
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(
    client_secret=client_secret, client_id=client_id)
sp = spotipy.Spotify(auth_manager=auth_manager)

artist = sp.artist('spotify:artist:3jOstUTkEu2JkjvRdBA5Gu')
print(artist)
