from dotenv import load_dotenv
import os
import base64
import json
from requests import post,get 

load_dotenv()

# Load in client id and client secret 

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    # Create the authorization string that you need to encode with base 64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # The URL we want to send the request to
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    

token = get_token()
for num in range(5):
    artist = input("Search for an artist: \n\t")
    result = search_for_artist(token, artist)
    # print(result["name"])
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    # print(songs)
    print("\nHere are the top 10 most popular songs for " + result["name"] + ". \n")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")


# Client Credentials Workflow: 
    # Spotify API allows us to query information about the Spotify library

# User Credentials Workflow: 
    # Another aspect of Spotify API allows you to control Spotify player and get information about user profile
    # This requires that you authenticate the individual user (Usually done through website or front-end UI)