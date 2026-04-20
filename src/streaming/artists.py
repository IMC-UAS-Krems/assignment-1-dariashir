"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
class Artist:
    def __init__(self, artist_id: str, name: str, genre: str):
        #storing basic artist information
        self.artist_id=artist_id
        self.name=name
        self.genre=genre
        self.tracks =[]

    def add_track(self, track):
        #adding a track to the artist's track list
        self.tracks.append(track)

    def track_count(self):
        #returning how many tracks the artist has
        return len(self.tracks)