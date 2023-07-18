from bs4 import BeautifulSoup
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print("Welcome to the Music Time Machine!")
date = input("Which year would you like to travel to? Enter the year in format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
billboard_data = response.text
soup = BeautifulSoup(billboard_data, "html.parser")
songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [title.getText().strip("\n\t") for title in songs]
artists = soup.find_all(name="span", class_="u-max-width-330")
artist_names = [name.getText().strip("\n\t") for name in artists]
song_and_artist = dict(zip(song_titles, artist_names))

print(song_and_artist)
print("\n")
print("Searching for songs on Spotify and creating new playlist...")

redirect_uri = "https://example.com"
scope = "playlist-modify-private"

OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIPY_REDIRECT_URI = "http://example.com"
SPOTIPY_SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(
auth_manager=SpotifyOAuth(
client_id=os.getenv("SPOTIPY_CLIENT_ID"),
client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
redirect_uri=SPOTIPY_REDIRECT_URI,
scope=SPOTIPY_SCOPE,
show_dialog=True,
cache_path="token.txt"
)
)
user_id = sp.current_user()["id"]

song_uris = []
for (song, artist) in song_and_artist.items():
    try:
        result = sp.search(q=f"track:{song} artist:{artist}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        pass

print(f"Number of songs found: {len(song_uris)}")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, )
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"New playlist '{date} Billboard 100' successfully created on Spotify!")