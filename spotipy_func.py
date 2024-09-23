"""
Spotify Utility Functions

This module provides a set of utility functions to interact with the Spotify Web API using the Spotipy library.
It includes functions to load the Spotify client, retrieve playlists and tracks, extract audio features, and more.

Modules:
    - load_spotify_client:  Loads Spotify client using credentials from a JSON configuration file.
    - get_my_playlists:     Retrieves all playlists of the current Spotify user.
    - get_tracks:           Retrieves all tracks from a specified playlist or the user saved ones.
    - get_audio_features:   Retrieves the audio features for a list of tracks.
    - extract_track_ids:    Extracts track IDs from a given playlist.
    - split_by_brackets:    Splits the input string by '[' and ']', ignoring empty results.
    - get_nested_value:     Retrieves the value from a nested dictionary based on a list of keys.
    - get_track_info:       Accesses all information from the extracted tracks by providing a list with all needed features.
    - merge_track_details_and_features: Combines track details with their corresponding audio features.
    - get_tracks_by_names_and_artists:  Retrieves tracks by their names and artist names.

Dependencies:
    - pandas
    - spotipy
    - re
    - json

Usage:
    Import this module and use the provided functions to interact with the Spotify Web API.

Author:
    Felix Romer
    
Date:
    2024-09-23
"""

import pandas as pd
import spotipy
import re
import json
from spotipy.oauth2 import SpotifyOAuth



def load_spotify_client(config_path: str, scope: str = "user-library-read") -> 'spotipy.Spotify':
    """
    Loads Spotify client using credentials from a JSON configuration file.

    This function reads the Spotify API credentials from a JSON file and sets up the Spotipy client
    with the necessary authentication.

    Args:
        config_path (str): The path to the JSON configuration file containing Spotify API credentials.
        scope (str, optional): The scope of access required for the Spotify API. Defaults to "user-library-read".

    Returns:
        sp (spotipy.Spotify): A Spotipy client instance authenticated with the provided credentials.
    """
    # Read and parse the JSON file
    with open(config_path, 'r') as file:
        config_data = json.load(file)

    # Load variables from config_data
    client_id       = config_data['client_id']
    client_secret   = config_data['client_secret']
    redirect_uri    = config_data['redirect_uri']

    # Set up the Spotipy API
    sp = spotipy.Spotify(
        auth_manager = SpotifyOAuth(
            client_id       = client_id,
            client_secret   = client_secret,
            redirect_uri    = redirect_uri,
            scope           = scope
        )
    )
    return sp



def get_my_playlists(sp: 'spotipy.Spotify') -> list:
    """
    Retrieves all playlists of the current Spotify user.

    This function fetches all playlists from the authenticated Spotify user using the Spotify Web API.
    It handles pagination to ensure all playlists are retrieved, returning them as a list.

    Args:
        sp (spotipy.Spotify): A Spotipy client instance used to interact with the Spotify API.

    Returns:
        playlists (list): A list of playlists, where each playlist is represented as a dictionary of its details.
    """

    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return playlists

def get_tracks(sp: 'spotipy.Spotify', playlist_id: str = None) -> list:
    """
    Retrieves all tracks from a specified playlist or the user saved ones.

    This function fetches all tracks from a given Spotify playlist by its ID, handling pagination 
    to ensure all tracks are retrieved.

    Args:
        sp (spotipy.Spotify): A Spotipy client instance used to interact with the Spotify API.
        playlist_id (str, optional): The Spotify ID of the playlist from which to retrieve tracks.

    Returns:
        tracks (list): A list of tracks, where each track is represented as a dictionary of its details.
    """
    tracks = []
    if playlist_id:
        results = sp.playlist_tracks(playlist_id)
    else:
        results = sp.current_user_saved_tracks(limit=50)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_audio_features(sp: 'spotipy.Spotify', track_ids: list) -> list:
    """
    Retrieves the audio features for a list of tracks.

    This function retrieves audio features for a batch of track IDs using the Spotify Web API.
    Since the API can handle up to 100 track IDs at a time, it batches the requests as necessary.

    Args:
        sp (spotipy.Spotify): A Spotipy client instance used to interact with the Spotify API.
        track_ids (list): A list of Spotify track IDs for which to retrieve audio features.

    Returns:
        audio_features (list): A list of audio feature dictionaries, where each dictionary contains features 
                                like danceability, energy, tempo, and more for a corresponding track.
    """
    audio_features = []
    # Spotify API can handle up to 100 track IDs at a time
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        audio_features.extend(sp.audio_features(batch))
    return audio_features

def extract_track_ids(sp: 'spotipy.Spotify', tracks: list) -> list:
    """
    Extracts track IDs from a given playlist.

    This function retrieves all tracks from the specified playlist and extracts the Spotify track IDs
    for each track that exists.

    Args:
        sp (spotipy.Spotify): A Spotipy client instance used to interact with the Spotify API.
        tracks (list): A list of tracks, where each track is represented as a dictionary of its details.

    Returns:
        list: A list of Spotify track IDs from the specified playlist.
    """

    track_ids = [item['track']['id'] for item in tracks if item['track']]
    return track_ids

def split_by_brackets(string: str) -> list:
    """Splits the input string by '[' and ']', ignoring empty results.

    Args:
        string (str): The string, that should be split.

    Returns:
        list: List with each string part as en element.
    
    """
    parts = re.split(r'[\[\]]', string)
    return [part for part in parts if part]

def get_nested_value(dic: dict, key_path: list):
    """
    Retrieves the value from a nested dictionary based on a list of keys.

    This function traverses a nested dictionary by iterating through a list of keys.
    For each key in the list, it drills down one level into the dictionary. 
    If the sequence of keys is valid, it returns the corresponding value.

    Args:
        dic (dict): The dictionary to search in. It can be a nested dictionary.
        key_path (list): A list of keys to access the nested value.

    Returns:
        value (any): The value located at the end of the key path. 
                    This could be any type (e.g., str, int, dict, list, etc.), 
                    depending on the structure of the dictionary.
    
    Example:
        dic = {'a': {'b': {'c': 10}}}

        key_path = ['a', 'b', 'c']
        
        get_nested_value(dic, key_path)

        #Returns: 10
    """
    
    value = dic
    for key in key_path:
        value = value[key]
    
    return value

def get_track_info(track: dict, features: list) -> list:
    """
    With this function all informations from the extracted tracks can be accessed easily,
    by providing a list with all needed features.

    """
    extracted_features = []
    for feature in features:
        key_path = split_by_brackets(feature)
        value    = get_nested_value(track, key_path)
        extracted_features.append(value)
    return  extracted_features

def merge_track_details_and_features(tracks: list, audio_features: list, playlist_name: str = None, extra_track_info: list = []) -> pd.DataFrame:
    """
    Combines track details with their corresponding audio features.

    This function takes the track details and their corresponding audio features and merges them into
    a single list of dictionaries containing track information and audio properties.

    Args:
        tracks (list): A list of track objects retrieved from a Spotify playlist.
        audio_features (list): A list of audio feature dictionaries, each corresponding to a track.
        playlist_name (str, optional): The name of the playlist without the suffix, used as the label for the track.
        extra_track_info (list[str], optional): Extra features from track information can be specified.
                                                e.g. ["[track][album][album_type]"]

    Returns:
        track_features (pd.DataFrame): A list of dictionaries, each containing detailed information about a track, 
                                        including its audio features.
    """
    track_list = []
    for item, features in zip(tracks, audio_features):
        if not item or not features:         # Ensure track and features are not None
            continue

        track = item['track']
        track_details = [item   ['added_at'],
                        track   ['name'],
                        track   ['id'],
                        track   ['artists'][0]['name'],
                        track   ['album']['name'],
                        track   ['popularity'],
                        features['danceability'],
                        features['energy'],
                        features['key'],
                        features['loudness'],
                        features['mode'],
                        features['speechiness'],
                        features['acousticness'],
                        features['instrumentalness'],
                        features['liveness'],
                        features['valence'],
                        features['tempo'],
                        features['duration_ms'],
                        features['time_signature'],
                        playlist_name
                        ]
        
        if extra_track_info:
            extra_features = get_track_info(item, extra_track_info)
            track_details += extra_features

        track_list.append(track_details)

    # Create DateFrame to store data
    column_names = ['added_at', 'track_name', 'track_id', 'artist', 'album', 'popularity', 'danceability',
                    'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                    'valence', 'tempo', 'duration_ms', 'time_signature', 'label'] + extra_track_info
    track_features = pd.DataFrame(track_list, columns = column_names)
    return track_features

def get_tracks_by_names_and_artists(sp: 'spotipy.Spotify', track_names: list, artist_names: list, time_points: list = []) -> list:
    """
    Retrieves tracks by their names and artist names.

    This function searches for multiple tracks on Spotify using the provided lists of track names and artist names.
    It returns a list of matching tracks found. Optionally, it can include time points for each track.

    Args:
        sp (spotipy.Spotify): A Spotipy client instance used to interact with the Spotify API.
        track_names (list): A list of track names.
        artist_names (list): A list of artist names.
        time_points (list, optional): A list of time points corresponding to each track. Defaults to None.

    Returns:
        list: A list of dictionaries, each containing the track details if found, otherwise None.
    """
    if len(track_names) != len(artist_names):
        raise ValueError("The length of track_names and artist_names must be the same.")
    if len(time_points) > 0 and len(track_names) != len(time_points):
        raise ValueError("The length of track_names and time_points must be the same if time_points is provided.")

    tracks = []
    for i, (track_name, artist_name) in enumerate(zip(track_names, artist_names)):
        query = f"track:{track_name} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        track_items = results.get('tracks', {}).get('items', [])
        # Append track details if found
        if track_items:
            song_format = {'added_at': time_points.iloc[i] if len(time_points) > 0 else None,
                           'track':    track_items[0]}
            tracks.append(song_format)
    return tracks
