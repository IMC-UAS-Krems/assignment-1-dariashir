"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import date
class User:
    def __init__(self, user_id:str, name:str, age:int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self,session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total_sec=0
        for each in self.sessions:
            total_sec += each.duration_listened_seconds
        return total_sec

    def total_listening_minutes(self):
        total_min=0
        total_min+=self.total_listening_seconds()/60
        return total_min

    def unique_tracks_listened(self):
        listed=[]
        for each in self.sessions:
            if each.track.track_id not in listed:
                listed.append(each.track.track_id)
        return set(listed)

class FamilyAccountUser(User):
    def __init__(self, user_id:str, name:str, age:int):
        super().__init__(user_id, name, age)
        self.sub_users=[]
    def add_sub_user(self,sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        members = []
        members.append(self)
        for user in self.sub_users:
            members.append(user)
        return members
class FamilyMember(User):
    def __init__(self,user_id:str,name:str,age:int,parent:FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent=parent

class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6
    def __init__(self,user_id:str,name:str,age:int):
        super().__init__(user_id,name,age)
class PremiumUser(User):
    def __init__(self,user_id:str,name:str,age:int,subscription_start:date):
        super().__init__(user_id, name, age)
        self.subscription_start=subscription_start
