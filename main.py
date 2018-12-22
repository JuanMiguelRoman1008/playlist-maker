# usage py main.py username

import os
import csv
import sys
import json
import spotipy
import random
import webbrowser
import configparser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the args from terminal
username = sys.argv[1]
scope = 'user-read-private playlist-modify-public'

# Erase cache and prompt user permission
try:
	token = util.prompt_for_user_token(username, scope)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

# Create Spotify Object
spotify = spotipy.Spotify(auth=token)

# Display my Credentials
user = spotify.current_user()

displayName = user['display_name']
profileURL = user['external_urls']['spotify']
print('Playlists made by:', displayName)
print('View them by going to:', profileURL)

# Read CSV File to get the names
with open('sample.csv','r') as f:
	rows = csv.DictReader(f)
	names = list(next(rows))

# Read CSV File to get the songs
songs = {}
with open('sample.csv','r') as f:
	rows = csv.DictReader(f)
	for r in rows:
		for name in names[1:]:
			if name not in songs:
				songs[name] = [r[name]]
			else:
				songs[name].append(r[name])

# Randomizes Dictionary
for song in songs:
	random.shuffle(songs[song])

# Turn songs to track id
tracks = {}
for song in songs:
	for track in songs[song]:
		trackID = spotify.search(q = track,limit = 1, offset = 0, type='track', market=None)
		if trackID['tracks']['total'] > 0:
			if song not in tracks:
				tracks[song] = [trackID['tracks']['items'][0]['id']]
			else:
				tracks[song].append(trackID['tracks']['items'][0]['id'])


# Creates playlists for each of my dudes
playlists = {}
for name in names[1:]:
	playlist_name = name
	playlist_description = 'Hi, ' + playlist_name + ' we made this for you! -Sibiscus <3'
	playlist = spotify.user_playlist_create(user=username ,name=playlist_name,public=True, description=playlist_description)
	playlists[name] = playlist['id']

# Populates Playlists with each of the songs 
for name in names[1:]:
	final = spotify.user_playlist_add_tracks(user = username, playlist_id = playlists[name], tracks = tracks[name])
