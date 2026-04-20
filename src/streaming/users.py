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
    # storing basic user info
    def __init__(self, user_id:str, name:str, age:int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self,session):
        #add a session to the user
        self.sessions.append(session)

    def total_listening_seconds(self):
        #counting total listening time in seconds
        total_sec=0
        for each in self.sessions:
            total_sec += each.duration_listened_seconds
        return total_sec

    def total_listening_minutes(self):
        total_min=0
        #converting total seconds into minutes
        total_min+=self.total_listening_seconds()/60
        return total_min

    def unique_tracks_listened(self):
        #returning all unique tracks id's the user listened to
        listed=[]
        for each in self.sessions:
            if each.track.track_id not in listed:
                listed.append(each.track.track_id)
        return set(listed)

class FamilyAccountUser(User):
    #the account which can have sub users
    def __init__(self, user_id:str, name:str, age:int):
        super().__init__(user_id, name, age)
        self.sub_users=[]

    def add_sub_user(self,sub_user):
        #adding a family member
        self.sub_users.append(sub_user)

    def all_members(self):
        members = []
        members.append(self)
        for user in self.sub_users:
            members.append(user)
            #returning main user and all sub users
        return members

class FamilyMember(User):
    #a user inside a family account
    def __init__(self,user_id:str,name:str,age:int,parent:FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent=parent

class FreeUser(User):
    #free version user with limitations
    MAX_SKIPS_PER_HOUR = 6
    def __init__(self,user_id:str,name:str,age:int):
        super().__init__(user_id,name,age)

class PremiumUser(User):
    #user with the subscription
    def __init__(self,user_id:str,name:str,age:int,subscription_start:date):
        super().__init__(user_id, name, age)
        self.subscription_start=subscription_start
