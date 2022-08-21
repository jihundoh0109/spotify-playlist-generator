import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


scope = ['user-top-read', 'playlist-modify-public', 'playlist-modify-private']
username = input("Please enter your Spotify username: ")

token = SpotifyOAuth(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                     client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
                     redirect_uri=os.environ.get('SPOTIFY_REDIRECT_URI'),
                     scope=scope)

spotify = spotipy.Spotify(auth_manager=token)
