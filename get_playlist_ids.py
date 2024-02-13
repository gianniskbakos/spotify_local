import pandas as pd
import os
import sys
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)
from functions import MySpotifyAPI
from params import get_spotify_auth_params

# Get Spotify API credentials
creds_ini_path, path_root_data, key_creds = get_spotify_auth_params()

# Initialize Spotify API wrapper
sp = MySpotifyAPI(path_root_data, creds_ini_path=creds_ini_path, key_creds=key_creds)

# Extract playlist ids and save to csv
for offset in [0]: # 100, 150, 200, 250, 300, 350, 400, 450]:
    res_json = sp.search_playlists(query="bachata", offset=offset)
    #print(f"Exampe of a json response:\n{res_json['playlists']['items'][1]}")

    playlist_id = []
    for i in range(len(res_json['playlists']['items'])):
        playlist_id.append(res_json['playlists']['items'][i]['id'])

df = pd.DataFrame({'playlist_id':playlist_id})
df.to_csv('playlist_ids.csv')