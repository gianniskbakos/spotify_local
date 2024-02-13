import configparser
import json
import requests
import spotipy

class SpotifyAPI:
    def __init__(self, path_root_data, creds_ini_path=None, key_creds="SpotifyAttest"):
        '''
        Initialize the SpotifyScraper class and authenticate.

        '''
        if creds_ini_path is not None:
            self.creds_ini_path = creds_ini_path
        self.path_root_data = path_root_data
        self.client_id = self.get_cred(key_creds, 'api_key')
        self.client_secret = self.get_cred(key_creds, 'api_secret')
        self.redirect_uri = "http://localhost:8080"
        self.token = self.get_token()

        self.sp = spotipy.Spotify(auth=self.token)

############################# credentials and authentication ####################################

    def get_cred(self, platform, cred_name):
        """
        Get credentials from creds.ini file.

        This assumes you have a creds.ini file with this format:

        [YourTitle_ForExampleSpotify]
        api_key = your_api_key
        api_secret = your_api_secret

        """

        config = configparser.ConfigParser()
        config.read(self.creds_ini_path)
        cred = config.get(platform, cred_name)
        return cred

    def get_token(self):
        """
        Get authentication token from Spotify API.
        """
        try:
            grant_type = 'client_credentials'
            body_params = {'grant_type': grant_type}
            url = 'https://accounts.spotify.com/api/token'
            response = requests.post(url, data=body_params, auth=(self.client_id, self.client_secret))
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            token_raw = json.loads(response.text)
            token = token_raw["access_token"]
            print("API authentication successful!")
            #print(f"Token: {token}")
            return token
        except requests.exceptions.RequestException as e:
            print(f"API authentication error: {e}")
            return None
