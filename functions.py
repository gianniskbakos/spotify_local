import os
from datetime import datetime
import requests
import pandas as pd
from SpotifyAPI import SpotifyAPI

class MySpotifyAPI(SpotifyAPI):
    def __init__(self, path_root_data, creds_ini_path, key_creds):
        super().__init__(path_root_data, creds_ini_path, key_creds)

    def search_playlists(self, query, offset):
        res_json = self.sp.search(q=query, type="playlist", limit=50, offset=offset)
        return res_json
        
    def get_artist_df(self, artist_id):
        """
        Makes the API call and reformats the json into a dataframe
        """
        res_json = self.sp.artist(artist_id) #this will return a json
        return res_json

    def get_artist_album_df(self, artist_id):
        """
        Makes the API call and reformats the json into a dataframe
        """
        res_json = self.sp.artist_albums(artist_id) #this will return a json
        return res_json

    def get_track(self, track_id):
        """
        Makes the API call and reformats the json into a dataframe
        """
        res_json = self.sp.track(track_id) #this will return a json
        return res_json
    def get_playlist(self, playlist_id):
        """
        Makes the API call and reformats the json into a dataframe
        """
        res_json = self.sp.playlist(playlist_id) #this will return a json
        return res_json
    
    def get_playlist_tracks(self, playlist_id, offset=0):
        """
        Makes the API call and reformats the json into a dataframe
        """
        res_json = self.sp.playlist_tracks(playlist_id, offset=offset) #this will return a json
        return res_json

    def save_to_csv(self, path_root, artist_id, tag_todays_date, df_out):
        path_folder = f"{path_root}SpotifyData/ByArtist/{artist_id}/"
        if not os.path.exists(path_folder):
            os.makedirs(path_folder);
            print('Created folder: ', path_folder)
        path = f"{path_folder}{tag_todays_date}.csv"
        df_out.to_csv(path, index=False);
        print("Saved: ", path)

    def get_and_save_artist_feats(self, artist_ids, path_root):
        tag_todays_date = datetime.now().strftime('%Y_%m_%d')

        for iTrack, artist_id in enumerate(artist_ids): #todo: refactor (is not track but artist)
            df_out, artist_json = self.get_artist_df(artist_id)
            self.save_to_csv(path_root, artist_id, tag_todays_date, df_out)

        return df_out, artist_json, iTrack

    #Alternative to "get_artist_df()", if you want to do the request without spotipy
    #can't remember if this works, i haven't re-tested
    def get_artist_df_WITHOUTSPOTIPY(self, artist_id, token):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"

        # The headers for the request
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url, headers=headers)
        res_json = response.json()
        return res_json