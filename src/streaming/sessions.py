"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
from streaming.users import User
from streaming.tracks import Track
from datetime import datetime
class ListeningSession:
    def __init__(self,session_id:str,user:User,track:Track,timestamp:datetime,duration_listened_seconds:int):
        # storing basic sessions info
        self.session_id=session_id
        self.user=user
        self.track=track
        self.timestamp=timestamp
        self.duration_listened_seconds=duration_listened_seconds
    def duration_listened_minutes(self):
        #converting seconds to minutes
        return self.duration_listened_seconds/60