"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from streaming.tracks import Track
from streaming.users import User
from streaming.artists import Artist
from streaming.albums import Album
from streaming.playlists import Playlist
from streaming.sessions import ListeningSession
from datetime import datetime
from datetime import datetime, timedelta
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.tracks import Song
class StreamingPlatform:
    def __init__(self, name:str):
        self.name=name
        self.catalogue={}
        self.users={}
        self.artists={}
        self.albums={}
        self.playlists={}
        self.sessions=[]

    def add_track(self, track: Track) -> None:
        track_id = track.track_id
        catalogue_dict = self.catalogue
        catalogue_dict[track_id] = track

    def add_user(self, user: User) -> None:
        user_id = user.user_id
        users_dict = self.users
        users_dict[user_id] = user

    def add_artist(self,artist:Artist) -> None:
        artist_id=artist.artist_id
        artists_dict=self.artists
        artists_dict[artist_id]=artist

    def add_album(self,album:Album) -> None:
        album_id=album.album_id
        albums_dict=self.albums
        albums_dict[album_id]=album

    def add_playlist(self,playlist:Playlist) ->None:
        playlist_id=playlist.playlist_id
        playlists_dict=self.playlists
        playlists_dict[playlist_id]=playlist

    def record_session(self, session: ListeningSession) -> None:
        sessions_list = self.sessions
        sessions_list.append(session)

    def get_track(self,track_id):
        catalogue_dict=self.catalogue
        track=catalogue_dict.get(track_id)
        return track

    def get_user(self,user_id):
        users_dict = self.users
        user = users_dict.get(user_id)
        return user

    def get_artist(self, artist_id):
        artists_dict = self.artists
        artist = artists_dict.get(artist_id)
        return artist

    def get_album(self, album_id):
        albums_dict = self.albums
        album = albums_dict.get(album_id)
        return album

    def all_users(self):
        users_dict = self.users
        users_list = list(users_dict.values())
        return users_list

    def all_tracks(self):
        catalogue_dict = self.catalogue
        tracks_list = list(catalogue_dict.values())
        return tracks_list



    def total_listening_time_minutes(self,start:datetime,end:datetime) -> float:
        total_seconds=0
        total=0
        for each in self.sessions:
            if each.timestamp >=start and each.timestamp <=end:
                total_seconds+=each.duration_listened_seconds
        total=total_seconds/60
        return total


    def avg_unique_tracks_per_premium_user(self, days=30) -> float:
        total_unique_tracks=0
        premium_users=0
        date=datetime.now()-timedelta(days=days)
        for user in self.users.values():
            if isinstance(user,PremiumUser):
                premium_users+=1
                unique_tracks=set()
                for session in self.sessions:
                    if session.user==user:
                        if session.timestamp >=date:
                            unique_tracks.add(session.track.track_id)
                total_unique_tracks+=len(unique_tracks)
        if premium_users==0:
            return float(0)
        avg= total_unique_tracks/premium_users
        return float(avg)


    def track_with_most_distinct_listeners(self) -> Track | None:
        if len(self.sessions) ==0:
            return None
        unique_listeners ={}
        for each in self.sessions:
            track_id=each.track.track_id
            user_id=each.user.user_id
            if track_id not in unique_listeners:
                listeners=set()
                unique_listeners[track_id]=listeners
            unique_listeners[track_id].add(user_id)
        max_listeners =0
        best_track_id =None
        for track_id in unique_listeners:
            listener_count=len(unique_listeners[track_id])
            if listener_count>max_listeners:
                max_listeners=listener_count
                best_track_id=track_id
        return self.catalogue.get(best_track_id)


    def avg_session_duration_by_user_type(self):
        user_types ={}
        for session in self.sessions:
            user=session.user
            if isinstance(user, FreeUser):
                user_type="FreeUser"
            elif isinstance(user, PremiumUser):
                user_type="PremiumUser"
            elif isinstance(user, FamilyAccountUser):
                user_type="FamilyAccountUser"
            elif isinstance(user, FamilyMember):
                user_type="FamilyMember"
            duration=session.duration_listened_seconds
            if user_type not in user_types:
                user_types[user_type] =[]
            user_types[user_type].append(duration)
        results =[]
        for user_type, durations in user_types.items():
            average=sum(durations)/len(durations)
            results.append((user_type,average))
        results=sorted(results,key=lambda x:x[1],reverse=True)
        return results

    def total_listening_time_underage_sub_users_minutes(self,age_threshold=18):
        total_seconds=0
        minutes=0
        for session in self.sessions:
            user=session.user
            if isinstance(user,FamilyMember):
                if user.age<age_threshold:
                    total_seconds+=session.duration_listened_seconds
        minutes=total_seconds/60
        return minutes

    def top_artists_by_listening_time(self, n=5):
        artist_and_tracks ={}
        for session in self.sessions:
            track=session.track
            if isinstance(track,Song):
                artist = track.artist
                if artist not in artist_and_tracks:
                    artist_and_tracks[artist] =0
                artist_and_tracks[artist]+=session.duration_listened_seconds
        total_list =[]
        for artist in artist_and_tracks:
            total_seconds=artist_and_tracks[artist]
            total_minutes=total_seconds/60
            total_list.append((artist,total_minutes))
        total_list=sorted(total_list, key=lambda x:x[1],reverse=True)
        return total_list[0:n]


