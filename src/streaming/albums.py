"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from streaming.artists import Artist
class Album:
    def __init__(self, album_id:str, title:str, artist:Artist, release_year:int):
        #storing basic album information
        self.album_id=album_id
        self.title=title
        self.artist=artist
        self.release_year=release_year
        self.tracks =[]

    def add_track(self, track):
        track.album =self
        self.tracks.append(track)
        #sorting tracks by track number
        self.tracks=sorted(self.tracks, key=lambda t: t.track_number)

    def track_ids(self):
        #returning a set of all tracks id's in this album
        return {t.track_id for t in self.tracks}

    def duration_seconds(self):
        #adding up the duration of all tracks and returning the total duration
        total=0
        for t in self.tracks:
            total+=t.duration_seconds
        return total