import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
import os
import json
import inquirer

scope = ['user-top-read', 'playlist-modify-public', 'playlist-modify-private']

def is_create_playlist_mode(prev_answers):
    return prev_answers['user_option'] == "Create a playlist with my top songs over the last 4 weeks"

# getting user inputs
questions = [
    inquirer.Text('username',
                   message="What's your Spotify username?"
                   ),
    inquirer.List('user_option',
                   message='What would you like to do?',
                   choices=['Create a playlist with my top songs over the last 4 weeks', 
                            'something else']
                   ),
    inquirer.List('playlist_type',
                   message='What kind of playlist would you like to create?',
                   choices=['Public', 'Private'],
                   ignore=lambda prev_answers: not is_create_playlist_mode(prev_answers)
                   ),
    inquirer.Text('num_songs',
                   message='How many top songs would you like in your playlist? (enter between 10 and 50)',
                   ignore=lambda prev_answers: not is_create_playlist_mode(prev_answers),
                   validate=lambda _, num: 10 <= int(num) <= 50,
                   )
]
answers = inquirer.prompt(questions)

# authorize app for access to user data 
token = SpotifyOAuth(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                    client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
                    redirect_uri=os.environ.get('SPOTIFY_REDIRECT_URI'),
                    scope=scope, username=answers['username'])
    
# Spotify API client
spotify = spotipy.Spotify(auth_manager=token)

if is_create_playlist_mode(answers):
    top_songs_data = spotify.current_user_top_tracks(limit=answers['num_songs'], time_range="short_term")
    playlist = spotify.user_playlist_create(user=answers['username'],
                                            name=f"My Top {answers['num_songs']} Songs",
                                            public=answers['playlist_type']=='Public')
    
    top_songs_uri = [track['uri'] for track in top_songs_data['items']]
    
    spotify.playlist_add_items(playlist_id=playlist['id'], items=top_songs_uri)
