import pandas as pd
import os
import sys
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)
from functions import MySpotifyAPI
from params import get_spotify_auth_params
from utils import data_prep as dp
import openpyxl as px

df_tracks = pd.read_csv('tracks.csv')
df_playlist_tracks = pd.read_csv('playlist_tracks.csv')
df_playlists = pd.read_csv('playlists.csv')

playlist_counts = df_playlist_tracks['Playlist_ID'].value_counts().sort_values(ascending=False).reset_index()

playlist_counts = pd.merge(playlist_counts, df_playlists, on='Playlist_ID', how='left')


playlist_track_comb = df_playlist_tracks.groupby(['Playlist_ID', 'Track_ID']).size().sort_values(ascending=False)
playlist_sample=playlist_counts[playlist_counts.Playlist_ID == '6Ha6YESGKippsZPXgg4tD0']
df_playlist_tracks_merged_temp = pd.merge(playlist_sample, df_playlist_tracks, on='Playlist_ID', how='left')
df_playlist_tracks_merged = pd.merge(df_playlist_tracks_merged_temp, df_tracks, on='Track_ID', how='left')
len(df_playlist_tracks_merged)

playlist_sample = df_playlist_tracks[(df_playlist_tracks['Playlist_ID']=='483a4E6LHwLdcDYy1VPrgM') & (df_playlist_tracks['Track_ID']=='5dl97w82KkuprJVDKSyJQp')]