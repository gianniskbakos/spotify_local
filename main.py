import pandas as pd
import os
import sys
from functions import MySpotifyAPI

script_dir = os.path.dirname(__file__)
src = script_dir
sys.path.append(script_dir)
#sys.path.append(os.path.join(script_dir, '..'))
from functions import * # get_and_save_artist_feats, search_playlists


# Authenticate to Spotify API
creds_ini_path = 'C:\\Users\\giann\\creds.ini'
path_root_data = ""
key_creds = "Spotify"
sp = MySpotifyAPI(path_root_data, creds_ini_path=creds_ini_path, key_creds=key_creds)
print(sp.token) #verify that it gives you a token

for offset in [0]: # 100, 150, 200, 250, 300, 350, 400, 450]:
    res_json = sp.search_playlists(query="bachata", offset=offset)

    print(res_json)

    # now you need to extract the track ids from the outputs, etc.

    #for each df_out, you can 
    for i_playlist in range(len(df_out.iloc[0]["playlists.items"])):
        playlist_id = df_out.iloc[0]["playlists.items"][i_playlist]['id']

        #get tracks from that playlist (new API call)