import pandas as pd
import os
import sys
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)
from functions import MySpotifyAPI
from params import get_spotify_auth_params
from utils import data_prep as dp
import openpyxl as px

# Get Spotify API credentials
creds_ini_path, path_root_data, key_creds = get_spotify_auth_params()

# Initialize Spotify API wrapper
sp = MySpotifyAPI(path_root_data, creds_ini_path=creds_ini_path, key_creds=key_creds)

# Extract playlist ids and save to csv
playlist_ids = pd.read_csv('playlist_ids.csv')['playlist_id'].tolist()
test_run = False

playlists = []
tracks = []
playlist_tracks = []
albums = []
artists = []
track_artists = []

for i, playlist_id in enumerate(playlist_ids):
    res_playlist = sp.get_playlist(playlist_id)
    playlist_id = res_playlist['id']
    user_id = res_playlist['owner']['id']
    playlist_name = res_playlist['name']
    playlist_path = res_playlist['external_urls']['spotify']
    offset = 0
    while True:
      res_tracks = sp.get_playlist_tracks(playlist_id, offset=offset)
      total = res_tracks['total']
      
      print('\n\n'+playlist_name +", "+ playlist_path )
      playlist_dict = {'Playlist_ID': playlist_id, 'User_ID': user_id, 'Name': playlist_name, 'Path': playlist_path}
      playlists.append(playlist_dict)
      
      for j, track in enumerate(res_tracks['items']):
          # Track
          track_added_at = track['added_at']
          is_local = track['is_local']

          track_details = track['track'] # this is where all the useful information extracted below is

          track_id = track_details['id']
          album_id = track_details['album']['id']
          track_name = track_details['name']
          track_duration = track_details['duration_ms']
          if is_local:
            track_url = None
          else:
            track_url = track_details['external_urls']['spotify']
          print('Playlist: '+ str(i+1) + '  - Track: ' +str(offset+j+1)+", "+track_name)
          track_dict = {'Track_ID': track_id, 'Album_ID': album_id, 'Name': track_name, 'Duration': track_duration, 'Track_added_at': track_added_at, 'Is_Local': is_local, 'URL': track_url}
          tracks.append(track_dict)
          playlist_tracks_dict = {'Playlist_ID': playlist_id, 'Track_ID': track_id, 'order': j+1}
          playlist_tracks.append(playlist_tracks_dict)
          
          # Album
          album_name = track_details['album']['name']
          album_type = track_details['album']['album_type']
          album_release_date = track_details['album']['release_date']
          album_artists = track_details['album']['artists']
          all_album_artist_ids = []
          for k in range(len(album_artists)):
            if k == 0:
              primary_album_artist_id = album_artists[k]['id']
            all_album_artist_ids.append(album_artists[k]['id'])
          album_dict = {'Album_ID': album_id, 'Artist_ID': primary_album_artist_id, 'Name': album_name, 'Type': album_type, 'Release_Date': album_release_date, 'All_Artist_IDs': all_album_artist_ids}
          albums.append(album_dict)
          
          for l, artist in enumerate(track_details['artists']):
            # Artists
            artist_id = artist['id']
            artist_name = artist['name']
            artist_dict = {'Artist_ID': artist_id, 'Name': artist_name}
            artists.append(artist_dict)
            #todo: add artist genres and other artist details from the artist endpoint

            # Track_Artists
            track_artist_dict = {'Track_ID': track_id, 'Artist_ID': artist_id}
            track_artists.append(track_artist_dict)
      if test_run and i==0:
            break
      offset += 100
      if offset > total:
          break

df_playlists = pd.DataFrame(playlists)
df_playlist_tracks = pd.DataFrame(playlist_tracks)
df_tracks = pd.DataFrame(tracks)
df_albums = pd.DataFrame(albums)
df_track_artists = pd.DataFrame(track_artists)
df_artists = pd.DataFrame(artists).drop_duplicates('Artist_ID')

if not test_run:
  df_playlists.to_csv('playlists.csv', index=False)
  df_tracks.to_csv('tracks.csv', index=False)
  df_playlist_tracks.to_csv('playlist_tracks.csv', index=False)
  df_albums.to_csv('albums.csv', index=False)
  df_track_artists.to_csv('track_artists.csv', index=False)
  df_artists.to_csv('artists.csv', index=False)
  

# Count tracks by name and order by count descending
top_tracks = df_tracks['Name'].value_counts().sort_values(ascending=False).head(100)
# output to excel in a format that displays the spanish accents
top_tracks.to_excel('top_tracks.xlsx', engine='openpyxl')

# For each track there is an album, and potentially multiple artists for the album

# Example of a playlist json response:
{
  "collaborative": False,
  "description": "",
  "external_urls": {
    "spotify": "https://open.spotify.com/playlist/4G1vKeCArQNZCl8wMvwvb8"
  },
  "followers": {
    "href": None,
    "total": 0
  },
  "href": "https://api.spotify.com/v1/playlists/4G1vKeCArQNZCl8wMvwvb8?locale=en-GB%2Cen%3Bq%3D0.9%2Cfr-FR%3Bq%3D0.8%2Cfr%3Bq%3D0.7%2Cen-US%3Bq%3D0.6",
  "id": "4G1vKeCArQNZCl8wMvwvb8",
  "images": [
    {
      "url": "https://mosaic.scdn.co/640/ab67616d00001e028a9b4bca0c021e44c5c7eac6ab67616d00001e02ac070ac46e0667551611b24eab67616d00001e02c9f744b0d62da795bc21d04aab67616d00001e02d688b951a19f48941682e026",
      "height": 640,
      "width": 640
    },
    {
      "url": "https://mosaic.scdn.co/300/ab67616d00001e028a9b4bca0c021e44c5c7eac6ab67616d00001e02ac070ac46e0667551611b24eab67616d00001e02c9f744b0d62da795bc21d04aab67616d00001e02d688b951a19f48941682e026",
      "height": 300,
      "width": 300
    },
    {
      "url": "https://mosaic.scdn.co/60/ab67616d00001e028a9b4bca0c021e44c5c7eac6ab67616d00001e02ac070ac46e0667551611b24eab67616d00001e02c9f744b0d62da795bc21d04aab67616d00001e02d688b951a19f48941682e026",
      "height": 60,
      "width": 60
    }
  ],
  "name": "Test playlist",
  "owner": {
    "external_urls": {
      "spotify": "https://open.spotify.com/user/21dd34f7jc57fco6osflyzwvi"
    },
    "href": "https://api.spotify.com/v1/users/21dd34f7jc57fco6osflyzwvi",
    "id": "21dd34f7jc57fco6osflyzwvi",
    "type": "user",
    "uri": "spotify:user:21dd34f7jc57fco6osflyzwvi",
    "display_name": "Giannis Bakos"
  },
  "public": true,
  "snapshot_id": "NywwM2FjOTg4MzkzYzFhZDg4YmJkM2EzOWE1Njg5NmNiMDUyNjdlMTg2",
  "tracks": {
    "href": "https://api.spotify.com/v1/playlists/4G1vKeCArQNZCl8wMvwvb8/tracks?offset=0&limit=100&locale=en-GB%2Cen%3Bq%3D0.9%2Cfr-FR%3Bq%3D0.8%2Cfr%3Bq%3D0.7%2Cen-US%3Bq%3D0.6",
    "limit": 100,
    "next": None,
    "offset": 0,
    "previous": None,
    "total": 4,
    "items": [
      {
        "added_at": "2024-02-13T17:36:55Z",
        "added_by": {
          "external_urls": {
            "spotify": "https://open.spotify.com/user/21dd34f7jc57fco6osflyzwvi"
          },
          "href": "https://api.spotify.com/v1/users/21dd34f7jc57fco6osflyzwvi",
          "id": "21dd34f7jc57fco6osflyzwvi",
          "type": "user",
          "uri": "spotify:user:21dd34f7jc57fco6osflyzwvi"
        },
        "is_local": False,
        "track": {
          "album": {
            "album_type": "single",
            "total_tracks": 1,
            "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
            "external_urls": {
              "spotify": "https://open.spotify.com/album/1TpGeAzOJgAGdPkcWl95r2"
            },
            "href": "https://api.spotify.com/v1/albums/1TpGeAzOJgAGdPkcWl95r2",
            "id": "1TpGeAzOJgAGdPkcWl95r2",
            "images": [
              {
                "url": "https://i.scdn.co/image/ab67616d0000b273c9f744b0d62da795bc21d04a",
                "height": 640,
                "width": 640
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00001e02c9f744b0d62da795bc21d04a",
                "height": 300,
                "width": 300
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00004851c9f744b0d62da795bc21d04a",
                "height": 64,
                "width": 64
              }
            ],
            "name": "La Bachata",
            "release_date": "2022-05-26",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:1TpGeAzOJgAGdPkcWl95r2",
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/0tmwSHipWxN12fsoLcFU3B"
                },
                "href": "https://api.spotify.com/v1/artists/0tmwSHipWxN12fsoLcFU3B",
                "id": "0tmwSHipWxN12fsoLcFU3B",
                "name": "Manuel Turizo",
                "type": "artist",
                "uri": "spotify:artist:0tmwSHipWxN12fsoLcFU3B"
              }
            ]
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0tmwSHipWxN12fsoLcFU3B"
              },
              "href": "https://api.spotify.com/v1/artists/0tmwSHipWxN12fsoLcFU3B",
              "id": "0tmwSHipWxN12fsoLcFU3B",
              "name": "Manuel Turizo",
              "type": "artist",
              "uri": "spotify:artist:0tmwSHipWxN12fsoLcFU3B"
            }
          ],
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "disc_number": 1,
          "duration_ms": 162637,
          "explicit": False,
          "external_ids": {
            "isrc": "QZDYA1800087"
          },
          "external_urls": {
            "spotify": "https://open.spotify.com/track/5ww2BF9slyYgNOk37BlC4u"
          },
          "href": "https://api.spotify.com/v1/tracks/5ww2BF9slyYgNOk37BlC4u",
          "id": "5ww2BF9slyYgNOk37BlC4u",
          "name": "La Bachata",
          "popularity": 85,
          "preview_url": "https://p.scdn.co/mp3-preview/0232b53fd7849e6696e1ab3099dd01dd00823f17?cid=d93feb37e7fc4a6ab03374965aa8588f",
          "track_number": 1,
          "type": "track",
          "uri": "spotify:track:5ww2BF9slyYgNOk37BlC4u",
          "is_local": False,
          "episode": False,
          "track": true
        },
        "primary_color": None,
        "video_thumbnail": {
          "url": None
        }
      },
      {
        "added_at": "2024-02-13T17:37:00Z",
        "added_by": {
          "external_urls": {
            "spotify": "https://open.spotify.com/user/21dd34f7jc57fco6osflyzwvi"
          },
          "href": "https://api.spotify.com/v1/users/21dd34f7jc57fco6osflyzwvi",
          "id": "21dd34f7jc57fco6osflyzwvi",
          "type": "user",
          "uri": "spotify:user:21dd34f7jc57fco6osflyzwvi"
        },
        "is_local": False,
        "track": {
          "album": {
            "album_type": "single",
            "total_tracks": 1,
            "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
            "external_urls": {
              "spotify": "https://open.spotify.com/album/4IBrn6DgPlaDKAv61FrW51"
            },
            "href": "https://api.spotify.com/v1/albums/4IBrn6DgPlaDKAv61FrW51",
            "id": "4IBrn6DgPlaDKAv61FrW51",
            "images": [
              {
                "url": "https://i.scdn.co/image/ab67616d0000b2738a9b4bca0c021e44c5c7eac6",
                "height": 640,
                "width": 640
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00001e028a9b4bca0c021e44c5c7eac6",
                "height": 300,
                "width": 300
              },
              {
                "url": "https://i.scdn.co/image/ab67616d000048518a9b4bca0c021e44c5c7eac6",
                "height": 64,
                "width": 64
              }
            ],
            "name": "Sola (Bachata Version)",
            "release_date": "2019-09-15",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:4IBrn6DgPlaDKAv61FrW51",
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/0Jc5bLNs5tbmmecIYaURND"
                },
                "href": "https://api.spotify.com/v1/artists/0Jc5bLNs5tbmmecIYaURND",
                "id": "0Jc5bLNs5tbmmecIYaURND",
                "name": "DJ Tony Pecino",
                "type": "artist",
                "uri": "spotify:artist:0Jc5bLNs5tbmmecIYaURND"
              }
            ]
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0Jc5bLNs5tbmmecIYaURND"
              },
              "href": "https://api.spotify.com/v1/artists/0Jc5bLNs5tbmmecIYaURND",
              "id": "0Jc5bLNs5tbmmecIYaURND",
              "name": "DJ Tony Pecino",
              "type": "artist",
              "uri": "spotify:artist:0Jc5bLNs5tbmmecIYaURND"
            }
          ],
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "disc_number": 1,
          "duration_ms": 186123,
          "explicit": False,
          "external_ids": {
            "isrc": "ushm91915113"
          },
          "external_urls": {
            "spotify": "https://open.spotify.com/track/3Drkw04CaWleDX8sNeelgC"
          },
          "href": "https://api.spotify.com/v1/tracks/3Drkw04CaWleDX8sNeelgC",
          "id": "3Drkw04CaWleDX8sNeelgC",
          "name": "Sola (Bachata Version)",
          "popularity": 45,
          "preview_url": "https://p.scdn.co/mp3-preview/37be887891cac4196bfba10790d902596d7e9728?cid=d93feb37e7fc4a6ab03374965aa8588f",
          "track_number": 1,
          "type": "track",
          "uri": "spotify:track:3Drkw04CaWleDX8sNeelgC",
          "is_local": False,
          "episode": False,
          "track": true
        },
        "primary_color": None,
        "video_thumbnail": {
          "url": None
        }
      },
      {
        "added_at": "2024-02-13T17:55:23Z",
        "added_by": {
          "external_urls": {
            "spotify": "https://open.spotify.com/user/21dd34f7jc57fco6osflyzwvi"
          },
          "href": "https://api.spotify.com/v1/users/21dd34f7jc57fco6osflyzwvi",
          "id": "21dd34f7jc57fco6osflyzwvi",
          "type": "user",
          "uri": "spotify:user:21dd34f7jc57fco6osflyzwvi"
        },
        "is_local": False,
        "track": {
          "album": {
            "album_type": "single",
            "total_tracks": 1,
            "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
            "external_urls": {
              "spotify": "https://open.spotify.com/album/4UDVt5eerRMk5hCMF1qek9"
            },
            "href": "https://api.spotify.com/v1/albums/4UDVt5eerRMk5hCMF1qek9",
            "id": "4UDVt5eerRMk5hCMF1qek9",
            "images": [
              {
                "url": "https://i.scdn.co/image/ab67616d0000b273ac070ac46e0667551611b24e",
                "height": 640,
                "width": 640
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00001e02ac070ac46e0667551611b24e",
                "height": 300,
                "width": 300
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00004851ac070ac46e0667551611b24e",
                "height": 64,
                "width": 64
              }
            ],
            "name": "Si Te Preguntan... (feat. Nicky Jam & Jay Wheeler)",
            "release_date": "2022-06-23",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:4UDVt5eerRMk5hCMF1qek9",
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/3MHaV05u0io8fQbZ2XPtlC"
                },
                "href": "https://api.spotify.com/v1/artists/3MHaV05u0io8fQbZ2XPtlC",
                "id": "3MHaV05u0io8fQbZ2XPtlC",
                "name": "Prince Royce",
                "type": "artist",
                "uri": "spotify:artist:3MHaV05u0io8fQbZ2XPtlC"
              },
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/1SupJlEpv7RS2tPNRaHViT"
                },
                "href": "https://api.spotify.com/v1/artists/1SupJlEpv7RS2tPNRaHViT",
                "id": "1SupJlEpv7RS2tPNRaHViT",
                "name": "Nicky Jam",
                "type": "artist",
                "uri": "spotify:artist:1SupJlEpv7RS2tPNRaHViT"
              },
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/2cPqdH7XMvwaBJEVjheH8g"
                },
                "href": "https://api.spotify.com/v1/artists/2cPqdH7XMvwaBJEVjheH8g",
                "id": "2cPqdH7XMvwaBJEVjheH8g",
                "name": "Jay Wheeler",
                "type": "artist",
                "uri": "spotify:artist:2cPqdH7XMvwaBJEVjheH8g"
              }
            ]
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/3MHaV05u0io8fQbZ2XPtlC"
              },
              "href": "https://api.spotify.com/v1/artists/3MHaV05u0io8fQbZ2XPtlC",
              "id": "3MHaV05u0io8fQbZ2XPtlC",
              "name": "Prince Royce",
              "type": "artist",
              "uri": "spotify:artist:3MHaV05u0io8fQbZ2XPtlC"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/1SupJlEpv7RS2tPNRaHViT"
              },
              "href": "https://api.spotify.com/v1/artists/1SupJlEpv7RS2tPNRaHViT",
              "id": "1SupJlEpv7RS2tPNRaHViT",
              "name": "Nicky Jam",
              "type": "artist",
              "uri": "spotify:artist:1SupJlEpv7RS2tPNRaHViT"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/2cPqdH7XMvwaBJEVjheH8g"
              },
              "href": "https://api.spotify.com/v1/artists/2cPqdH7XMvwaBJEVjheH8g",
              "id": "2cPqdH7XMvwaBJEVjheH8g",
              "name": "Jay Wheeler",
              "type": "artist",
              "uri": "spotify:artist:2cPqdH7XMvwaBJEVjheH8g"
            }
          ],
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "disc_number": 1,
          "duration_ms": 223073,
          "explicit": False,
          "external_ids": {
            "isrc": "QZUFT2210003"
          },
          "external_urls": {
            "spotify": "https://open.spotify.com/track/20yLo8tCAM1LXixAdBf3f2"
          },
          "href": "https://api.spotify.com/v1/tracks/20yLo8tCAM1LXixAdBf3f2",
          "id": "20yLo8tCAM1LXixAdBf3f2",
          "name": "Si Te Preguntan... - feat. Nicky Jam & Jay Wheeler",
          "popularity": 69,
          "preview_url": "https://p.scdn.co/mp3-preview/78319aad33f96737ef89244eacd82cf42e5a0b27?cid=d93feb37e7fc4a6ab03374965aa8588f",
          "track_number": 1,
          "type": "track",
          "uri": "spotify:track:20yLo8tCAM1LXixAdBf3f2",
          "is_local": False,
          "episode": False,
          "track": true
        },
        "primary_color": None,
        "video_thumbnail": {
          "url": None
        }
      },
      {
        "added_at": "2024-02-13T17:55:27Z",
        "added_by": {
          "external_urls": {
            "spotify": "https://open.spotify.com/user/21dd34f7jc57fco6osflyzwvi"
          },
          "href": "https://api.spotify.com/v1/users/21dd34f7jc57fco6osflyzwvi",
          "id": "21dd34f7jc57fco6osflyzwvi",
          "type": "user",
          "uri": "spotify:user:21dd34f7jc57fco6osflyzwvi"
        },
        "is_local": False,
        "track": {
          "album": {
            "album_type": "album",
            "total_tracks": 25,
            "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
            "external_urls": {
              "spotify": "https://open.spotify.com/album/3Fk8yQvPlCHgwR2pNhEIRA"
            },
            "href": "https://api.spotify.com/v1/albums/3Fk8yQvPlCHgwR2pNhEIRA",
            "id": "3Fk8yQvPlCHgwR2pNhEIRA",
            "images": [
              {
                "url": "https://i.scdn.co/image/ab67616d0000b273d688b951a19f48941682e026",
                "height": 640,
                "width": 640
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00001e02d688b951a19f48941682e026",
                "height": 300,
                "width": 300
              },
              {
                "url": "https://i.scdn.co/image/ab67616d00004851d688b951a19f48941682e026",
                "height": 64,
                "width": 64
              }
            ],
            "name": "Don Juan",
            "release_date": "2023-08-25",
            "release_date_precision": "day",
            "type": "album",
            "uri": "spotify:album:3Fk8yQvPlCHgwR2pNhEIRA",
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau"
                },
                "href": "https://api.spotify.com/v1/artists/1r4hJ1h58CWwUQe3MxPuau",
                "id": "1r4hJ1h58CWwUQe3MxPuau",
                "name": "Maluma",
                "type": "artist",
                "uri": "spotify:artist:1r4hJ1h58CWwUQe3MxPuau"
              }
            ]
          },
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau"
              },
              "href": "https://api.spotify.com/v1/artists/1r4hJ1h58CWwUQe3MxPuau",
              "id": "1r4hJ1h58CWwUQe3MxPuau",
              "name": "Maluma",
              "type": "artist",
              "uri": "spotify:artist:1r4hJ1h58CWwUQe3MxPuau"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/4wLXwxDeWQ8mtUIRPxGiD6"
              },
              "href": "https://api.spotify.com/v1/artists/4wLXwxDeWQ8mtUIRPxGiD6",
              "id": "4wLXwxDeWQ8mtUIRPxGiD6",
              "name": "Marc Anthony",
              "type": "artist",
              "uri": "spotify:artist:4wLXwxDeWQ8mtUIRPxGiD6"
            }
          ],
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "disc_number": 1,
          "duration_ms": 267016,
          "explicit": False,
          "external_ids": {
            "isrc": "USSD12300008"
          },
          "external_urls": {
            "spotify": "https://open.spotify.com/track/7oGpwtUeck1XjVevuNWmFL"
          },
          "href": "https://api.spotify.com/v1/tracks/7oGpwtUeck1XjVevuNWmFL",
          "id": "7oGpwtUeck1XjVevuNWmFL",
          "name": "La Fórmula",
          "popularity": 60,
          "preview_url": "https://p.scdn.co/mp3-preview/1d1ec885c6c60d7bfdc294774e7dba3a24acb379?cid=d93feb37e7fc4a6ab03374965aa8588f",
          "track_number": 23,
          "type": "track",
          "uri": "spotify:track:7oGpwtUeck1XjVevuNWmFL",
          "is_local": False,
          "episode": False,
          "track": true
        },
        "primary_color": None,
        "video_thumbnail": {
          "url": None
        }
      }
    ]
  },
  "type": "playlist",
  "uri": "spotify:playlist:4G1vKeCArQNZCl8wMvwvb8",
  "primary_color": None
}