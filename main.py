import requests
import json
from googleapiclient.discovery import build
spotify_token = // your spotify token goes here //


class CreatePlaylist:
    def __init__(self):
        self.playlistId = // your YouTube playlist goes here //
        self.user_id = // your YouTube ID goes here //
        self.yt_song_list = []
        self.uri_list = []
        self.uri_dict = {}

    def retrieve_youtube_songs(self):
        """Retrieve "Liked YouTube Videos" video titles"""
        yt_api_key = // your YouTube api key goes here //

        youtube_constructor = build("youtube", "v3", developerKey=yt_api_key)

        results = youtube_constructor.playlistItems().list(
            playlistId=self.playlistId,
            part="snippet",
            maxResults=10
        ).execute()

        amount_songs = results["pageInfo"]["totalResults"]

        for i in range(amount_songs):
            self.yt_song_list.append(results["items"][i]["snippet"]["title"])
        
        // Error logging
        print(self.yt_song_list)

        return self.yt_song_list

    def search_songs_spotify(self):
        """Manually search video titles to retrieve URIs"""
        self.retrieve_youtube_songs()

        for i in self.yt_song_list:
            search_query = "https://api.spotify.com/v1/search?query=track%3A{}&type=track&offset=0&limit=1".format(i)

            json_response = requests.get(
                search_query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )
            
            // Error logging
            print("Response for each song search on Spotify:", json_response)

            response = json_response.json()
            
            self.uri_list.append(response["tracks"]["items"][0]["uri"])

        self.uri_dict["uris"] = self.uri_list

        return self.uri_dict

    def create_blank_playlist(self):
        """Create blank playlist on Spotify"""
        blank_query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)

        requests_body = json.dumps(
            {
                "name": "Playlist Jhizzle",
                "description": "New playlist created using Python",
                "public": True
            }
        )

        json_response = requests.post(
            blank_query,
            data=requests_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        
        // Error logging
        print("Response for blank playlist creation on Spotify:", json_response)

        response = json_response.json()

        blank_playlist_id = response["id"]

        return blank_playlist_id

    def add_songs_blank_playlist(self):
        self.search_songs_spotify()
        create_blank = self.create_blank_playlist()

        add_query = "https://api.spotify.com/v1/playlists/{}/tracks".format(create_blank)

        request_data = json.dumps(self.uri_dict)

        json_response = requests.post(
            add_query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        
        // Error logging
        print("Response for adding songs to blank playlist on Spotify:", json_response)


obj = CreatePlaylist()
obj.add_songs_blank_playlist()
