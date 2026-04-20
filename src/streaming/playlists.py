"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id: str, name: str, owner):
        #storing basic playlist info
        self.playlist_id = playlist_id
        self.name=name
        self.owner=owner
        self.tracks =[]

    def add_track(self, track):
        #adding tracks only if the track isn't in the playlist
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id):
        #finding the track by its id and removing it
        for track in self.tracks:
            if track.track_id==track_id:
                self.tracks.remove(track)
                break

    def total_duration_seconds(self):
        #adding all together the duration and returning the total
        total=0
        for track in self.tracks:
            total+=track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner):
        #inheriting playlist fields from the parent class
        super().__init__(playlist_id, name, owner)
        self.contributors=[owner]

    def add_contributor(self, user):
        #adding user to contributors if it's not there
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user is self.owner:
            return
        # removing user if it's in the contributors list
        if user in self.contributors:
            self.contributors.remove(user)