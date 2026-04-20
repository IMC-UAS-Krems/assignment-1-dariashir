"""
test_public.py
--------------
Public test suite template.

This file provides a minimal framework and examples to guide you in writing
comprehensive tests for your StreamingPlatform implementation. Each test class
corresponds to one of the 10 query methods (Q1-Q10).

You should:
1. Study the examples provided
2. Complete the stub tests (marked with TODO or pass statements)
3. Add additional test cases for edge cases and boundary conditions
4. Verify your implementation passes all tests

Run with:
    pytest tests/test_public.py -v
"""

import pytest
from datetime import datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.playlists import CollaborativePlaylist
from tests.conftest import FIXED_NOW, RECENT, OLD
from streaming.sessions import ListeningSession
from streaming.artists import Artist
from streaming.tracks import SingleRelease
from datetime import date
from streaming.playlists import Playlist


# ===========================================================================
# Q1 - Total cumulative listening time for a given period
# ===========================================================================

class TestTotalListeningTime:
    """Test the total_listening_time_minutes(start, end) method.
    
    This method should sum up all session durations that fall within
    the specified datetime window (inclusive on both ends).
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        start = RECENT - timedelta(hours=1)
        end = FIXED_NOW
        result = platform.total_listening_time_minutes(start, end)
        assert isinstance(result, float)

    def test_empty_window_returns_zero(self, platform: StreamingPlatform) -> None:
        """Test that a time window with no sessions returns 0.0."""
        far_future = FIXED_NOW + timedelta(days=365)
        result = platform.total_listening_time_minutes(
            far_future, far_future + timedelta(hours=1)
        )
        assert result == 0.0

    # TODO: Add a test that verifies the correct value for a known time period.
    #       Calculate the expected total based on the fixture data in conftest.py.
    def test_known_period_value(self, platform: StreamingPlatform) -> None:
        user_1=platform.get_user("u1")
        user_2=platform.get_user("u2")
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        t3=platform.get_track("t3")
        s1=ListeningSession("s1",user_1,t1,RECENT,120)
        s2=ListeningSession("s2",user_2,t2,FIXED_NOW,180)
        s3=ListeningSession("s3",user_1,t3,OLD,300)
        platform.record_session(s1)
        platform.record_session(s2)
        platform.record_session(s3)
        start=RECENT-timedelta(hours=1)
        end=FIXED_NOW
        result=platform.total_listening_time_minutes(start,end)
        assert result==5.0


# ===========================================================================
# Q2 - Average unique tracks per PremiumUser in the last N days
# ===========================================================================

class TestAvgUniqueTracksPremium:
    """Test the avg_unique_tracks_per_premium_user(days) method.
    
    This method should:
    - Count distinct tracks per PremiumUser in the last N days
    - Exclude FreeUser, FamilyAccountUser, and FamilyMember
    - Return 0.0 if there are no premium users
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.avg_unique_tracks_per_premium_user(days=30)
        assert isinstance(result, float)

    def test_no_premium_users_returns_zero(self) -> None:
        """Test with a platform that has no premium users."""
        p = StreamingPlatform("EmptyPlatform")
        p.add_user(FreeUser("u99", "Nobody", age=25))
        assert p.avg_unique_tracks_per_premium_user() == 0.0

    # TODO: Add a test with the fixture platform that verifies the correct
    #       average for premium users. You'll need to count unique tracks
    #       per premium user and calculate the average.
    def test_correct_value(self, platform: StreamingPlatform) -> None:
        user_1=platform.get_user("u2")
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        t3=platform.get_track("t3")
        s1=ListeningSession("s1", user_1, t1, RECENT, 120)
        s2=ListeningSession("s2", user_1, t2, RECENT, 150)
        s3=ListeningSession("s3", user_1, t2, RECENT, 180)
        s4=ListeningSession("s4", user_1, t3, OLD, 200)
        platform.record_session(s1)
        platform.record_session(s2)
        platform.record_session(s3)
        platform.record_session(s4)
        result=platform.avg_unique_tracks_per_premium_user(days=30)
        assert result==2.0


# ===========================================================================
# Q3 - Track with the most distinct listeners
# ===========================================================================

class TestTrackMostDistinctListeners:
    """Test the track_with_most_distinct_listeners() method.
    
    This method should:
    - Count the number of unique users who have listened to each track
    - Return the track with the highest count
    - Return None if the platform has no sessions
    """

    def test_empty_platform_returns_none(self) -> None:
        """Test that an empty platform returns None."""
        p = StreamingPlatform("Empty")
        assert p.track_with_most_distinct_listeners() is None

    # TODO: Add a test that verifies the correct track is returned.
    #       Count listeners per track from the fixture data.


    def test_correct_track(self, platform: StreamingPlatform) -> None:
        user_1=platform.get_user("u1")
        user_2=platform.get_user("u2")
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        s1=ListeningSession("s1",user_1,t1,RECENT,100)
        s2=ListeningSession("s2",user_2,t1,RECENT,120)
        s3=ListeningSession("s3",user_1,t2,RECENT,90)
        platform.record_session(s1)
        platform.record_session(s2)
        platform.record_session(s3)
        result=platform.track_with_most_distinct_listeners()
        assert result.track_id=="t1"




# ===========================================================================
# Q4 - Average session duration per user subtype, ranked
# ===========================================================================

class TestAvgSessionDurationByType:
    """Test the avg_session_duration_by_user_type() method.
    
    This method should:
    - Calculate average session duration (in seconds) for each user type
    - Return a list of (type_name, average_duration) tuples
    - Sort results from longest to shortest duration
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (str, float) tuples."""
        result = platform.avg_session_duration_by_user_type()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], str) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by duration (longest first)."""
        result = platform.avg_session_duration_by_user_type()
        durations = [r[1] for r in result]
        assert durations == sorted(durations, reverse=True)

    # TODO: Add tests to verify all user types are present and have correct averages.
    def test_all_user_types_present(self, platform: StreamingPlatform) -> None:
        user_1 = platform.get_user("u1")
        user_2 = platform.get_user("u2")
        t1 = platform.get_track("t1")
        t2 = platform.get_track("t2")
        s1 = ListeningSession("s1", user_1, t1, RECENT, 60)
        s2 = ListeningSession("s2", user_1, t2, RECENT, 120)
        s3 = ListeningSession("s3", user_2, t1, RECENT, 180)
        s4 = ListeningSession("s4", user_2, t2, RECENT, 240)
        platform.record_session(s1)
        platform.record_session(s2)
        platform.record_session(s3)
        platform.record_session(s4)
        result = platform.avg_session_duration_by_user_type()
        result_dict = {}
        for user_type, average in result:
            result_dict[user_type] = average
        assert "FreeUser" in result_dict
        assert "PremiumUser" in result_dict
        assert result_dict["FreeUser"] == 90.0
        assert result_dict["PremiumUser"] == 210.0


# ===========================================================================
# Q5 - Total listening time for underage sub-users
# ===========================================================================

class TestUnderageSubUserListening:
    """Test the total_listening_time_underage_sub_users_minutes(age_threshold) method.
    
    This method should:
    - Count only sessions for FamilyMember users under the age threshold
    - Convert to minutes
    - Return 0.0 if no underage users or their sessions exist
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.total_listening_time_underage_sub_users_minutes()
        assert isinstance(result, float)

    def test_no_family_users(self) -> None:
        """Test a platform with no family accounts."""
        p = StreamingPlatform("NoFamily")
        p.add_user(FreeUser("u1", "Solo", age=20))
        assert p.total_listening_time_underage_sub_users_minutes() == 0.0

    # TODO: Add tests for correct values with default and custom thresholds.
    def test_correct_value_default_threshold(self, platform: StreamingPlatform) -> None:
        user_1 = FamilyAccountUser("u3", "Parent", age=40)
        user_2 = FamilyMember("u4", "Teen", age=15, parent=user_1)
        platform.add_user(user_1)
        platform.add_user(user_2)
        artist = Artist("a2", "Rock Artist", genre="rock")
        track = SingleRelease("t4", "Rock Song", 200, "rock", artist,date(2023,1,1))
        platform.add_artist(artist)
        platform.add_track(track)
        artist.add_track(track)
        platform.record_session(ListeningSession("s1", user_2, track, RECENT, 120))
        platform.record_session(ListeningSession("s2", user_2, track, RECENT, 180))
        result = platform.total_listening_time_underage_sub_users_minutes()
        assert result == 5.0


    def test_custom_threshold(self, platform: StreamingPlatform) -> None:
        parent = FamilyAccountUser("u3", "name_1", age=40)
        child1 = FamilyMember("u4", "name_2", age=15, parent=parent)
        child2 = FamilyMember("u5", "name_3", age=19, parent=parent)
        platform.add_user(parent)
        platform.add_user(child1)
        platform.add_user(child2)
        artist = Artist("a2", "name_4", genre="rock")
        platform.add_artist(artist)
        track = SingleRelease("t4", "title_1", 200, "rock", artist,date(2023,1,1))
        platform.add_track(track)
        artist.add_track(track)
        session1 = ListeningSession("s1", child1, track, RECENT, 120)
        session2 = ListeningSession("s2", child2, track, RECENT, 180)
        platform.record_session(session1)
        platform.record_session(session2)
        result = platform.total_listening_time_underage_sub_users_minutes(age_threshold=21)
        assert result == 5.0


# ===========================================================================
# Q6 - Top N artists by total listening time
# ===========================================================================

class TestTopArtistsByListeningTime:
    """Test the top_artists_by_listening_time(n) method.
    
    This method should:
    - Rank artists by total cumulative listening time (minutes)
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return a list of (Artist, minutes) tuples
    - Sort from highest to lowest listening time
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (Artist, float) tuples."""
        from streaming.artists import Artist
        result = platform.top_artists_by_listening_time(n=3)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], Artist) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by listening time (highest first)."""
        result = platform.top_artists_by_listening_time(n=5)
        minutes = [r[1] for r in result]
        assert minutes == sorted(minutes, reverse=True)

    def test_respects_n_parameter(self, platform: StreamingPlatform) -> None:
        """Verify only the top N artists are returned."""
        result = platform.top_artists_by_listening_time(n=2)
        assert len(result) <= 2

    # TODO: Add a test that verifies the correct artists and values.
    def test_top_artist(self, platform: StreamingPlatform) -> None:
        user_1=platform.get_user("u1")
        user_2=platform.get_user("u2")
        artist2=Artist("a2","Waves",genre="rock")
        platform.add_artist(artist2)
        track_new=SingleRelease("t4", "Song", 200, "rock", artist2, date(2023, 1,1))
        platform.add_track(track_new)
        artist2.add_track(track_new)
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        platform.record_session(ListeningSession("s1",user_1,t1,RECENT,180))
        platform.record_session(ListeningSession("s2",user_2,t2, RECENT,210))
        platform.record_session(ListeningSession("s3",user_1,track_new,RECENT,100))
        result=platform.top_artists_by_listening_time(n=5)
        top_artist=result[0][0]
        listening_time=result[0][1]
        assert top_artist.artist_id=="a1"
        assert listening_time==6.5



# ===========================================================================
# Q7 - User's top genre and percentage
# ===========================================================================

class TestUserTopGenre:
    """Test the user_top_genre(user_id) method.
    
    This method should:
    - Find the genre with the most listening time for a user
    - Return (genre_name, percentage_of_total_time)
    - Return None if user doesn't exist or has no sessions
    """

    def test_returns_tuple_or_none(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a tuple or None."""
        result = platform.user_top_genre("u1")
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 2
            assert isinstance(result[0], str) and isinstance(result[1], float)

    def test_nonexistent_user_returns_none(self, platform: StreamingPlatform) -> None:
        """Test that a nonexistent user ID returns None."""
        assert platform.user_top_genre("does_not_exist") is None

    def test_percentage_in_valid_range(self, platform: StreamingPlatform) -> None:
        """Verify percentage is between 0 and 100."""
        for user in platform.all_users():
            result = platform.user_top_genre(user.user_id)
            if result is not None:
                _, pct = result
                assert 0.0 <= pct <= 100.0

    # TODO: Add a test that verifies the correct genre and percentage for a known user.
    def test_correct_top_genre(self, platform: StreamingPlatform) -> None:
        user_1=platform.get_user("u2")
        artist=Artist("a2","Artist",genre="rock")
        platform.add_artist(artist)
        track=SingleRelease("t4","Song",200, "rock", artist, date(2023, 1, 1))
        platform.add_track(track)
        artist.add_track(track)
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        platform.record_session(ListeningSession("s1",user_1,t1,RECENT,180))
        platform.record_session(ListeningSession("s2",user_1,t2,RECENT,210))
        platform.record_session(ListeningSession("s3",user_1,track,RECENT,100))
        result=platform.user_top_genre("u2")
        top_genre=result[0]
        percentage=result[1]
        expected_percentage = (390 / 490) * 100
        assert top_genre == "pop"
        assert percentage == expected_percentage


# ===========================================================================
# Q8 - CollaborativePlaylists with more than threshold distinct artists
# ===========================================================================

class TestCollaborativePlaylistsManyArtists:
    """Test the collaborative_playlists_with_many_artists(threshold) method.
    
    This method should:
    - Return all CollaborativePlaylist instances with >threshold distinct artists
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return playlists in registration order
    """

    def test_returns_list_of_collaborative_playlists(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a list of CollaborativePlaylist objects."""
        result = platform.collaborative_playlists_with_many_artists()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, CollaborativePlaylist)

    def test_higher_threshold_returns_empty(
        self, platform: StreamingPlatform
    ) -> None:
        """Test that a high threshold returns an empty list."""
        result = platform.collaborative_playlists_with_many_artists(threshold=100)
        assert result == []

    # TODO: Add tests that verify the correct playlists are returned with
    #       different threshold values.
    def test_default_threshold(self, platform: StreamingPlatform) -> None:
        owner=platform.get_user("u1")
        artist1=Artist("a2", "Waves", genre="rock")
        artist2=Artist("a3", "Skyline", genre="jazz")
        artist3=Artist("a4", "Echo", genre="electronic")
        platform.add_artist(artist1)
        platform.add_artist(artist2)
        platform.add_artist(artist3)
        track1=SingleRelease("t4", "Song1", 200, "rock", artist1, date(2023, 1, 1))
        track2=SingleRelease("t5", "Song2", 210, "jazz", artist2, date(2023, 1, 1))
        track3=SingleRelease("t6", "Song3", 220, "electronic", artist3, date(2023,1,1))
        platform.add_track(track1)
        platform.add_track(track2)
        platform.add_track(track3)
        artist1.add_track(track1)
        artist2.add_track(track2)
        artist3.add_track(track3)
        playlist1=CollaborativePlaylist("p1","Big Mix",owner)
        playlist1.add_track(platform.get_track("t1"))
        playlist1.add_track(track1)
        playlist1.add_track(track2)
        playlist1.add_track(track3)
        playlist2 = CollaborativePlaylist("p2","Small Mix",owner)
        playlist2.add_track(platform.get_track("t1"))
        playlist2.add_track(track1)
        platform.add_playlist(playlist1)
        platform.add_playlist(playlist2)
        result=platform.collaborative_playlists_with_many_artists()
        assert playlist1 in result
        assert playlist2 not in result


# ===========================================================================
# Q9 - Average tracks per playlist type
# ===========================================================================

class TestAvgTracksPerPlaylistType:
    """Test the avg_tracks_per_playlist_type() method.
    
    This method should:
    - Calculate average track count for standard Playlist instances
    - Calculate average track count for CollaborativePlaylist instances
    - Return a dict with keys "Playlist" and "CollaborativePlaylist"
    - Return 0.0 for types with no instances
    """

    def test_returns_dict_with_both_keys(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a dict with both playlist types."""
        result = platform.avg_tracks_per_playlist_type()
        assert isinstance(result, dict)
        assert "Playlist" in result
        assert "CollaborativePlaylist" in result

    # TODO: Add tests that verify the correct averages for each playlist type.
    def test_standard_playlist_average(self, platform: StreamingPlatform) -> None:
        owner = platform.get_user("u1")
        p1 = Playlist("p1", "name_1", owner)
        p2 = Playlist("p2", "name_2", owner)
        track1 = platform.get_track("t1")
        track2 = platform.get_track("t2")
        track3 = platform.get_track("t3")
        p1.add_track(track1)
        p1.add_track(track2)
        p2.add_track(track1)
        p2.add_track(track2)
        p2.add_track(track3)
        platform.add_playlist(p1)
        platform.add_playlist(p2)
        result = platform.avg_tracks_per_playlist_type()
        assert result["Playlist"] == 2.5

    def test_collaborative_playlist_average(self, platform: StreamingPlatform) -> None:
        owner=platform.get_user("u1")
        track1=platform.get_track("t1")
        track2=platform.get_track("t2")
        track3=platform.get_track("t3")
        playlist1=CollaborativePlaylist("p3","name_1",owner)
        playlist2=CollaborativePlaylist("p4","name_2",owner)
        playlist1.add_track(track1)
        playlist2.add_track(track1)
        playlist2.add_track(track2)
        playlist2.add_track(track3)
        platform.add_playlist(playlist1)
        platform.add_playlist(playlist2)
        result=platform.avg_tracks_per_playlist_type()
        average=result["CollaborativePlaylist"]
        assert average==2.0

# ===========================================================================
# Q10 - Users who completed at least one full album
# ===========================================================================

class TestUsersWhoCompletedAlbums:
    """Test the users_who_completed_albums() method.
    
    This method should:
    - Return users who have listened to every track on at least one album
    - Return (User, [album_titles]) tuples
    - Include all completed albums for each user
    - Ignore albums with no tracks
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (User, list) tuples."""
        from streaming.users import User
        result = platform.users_who_completed_albums()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], User) and isinstance(item[1], list)

    def test_completed_album_titles_are_strings(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify all completed album titles are strings."""
        result = platform.users_who_completed_albums()
        for _, titles in result:
            assert all(isinstance(t, str) for t in titles)

    # TODO: Add tests that verify the correct users and albums are identified.
    def test_correct_users_identified(self, platform: StreamingPlatform) -> None:
        user_2=platform.get_user("u1")
        user_1=platform.get_user("u2")
        track1=platform.get_track("t1")
        track2=platform.get_track("t2")
        track3=platform.get_track("t3")
        platform.record_session(ListeningSession("s1",user_1,track1,RECENT,180))
        platform.record_session(ListeningSession("s2",user_1,track2,RECENT,210))
        platform.record_session(ListeningSession("s3",user_1,track3,RECENT,195))
        platform.record_session(ListeningSession("s4",user_2,track1,RECENT,180))
        platform.record_session(ListeningSession("s5",user_2,track2,RECENT,210))
        result = platform.users_who_completed_albums()
        user_ids = []
        for user, albums in result:
            user_ids.append(user.user_id)
        assert "u2" in user_ids
        assert "u1" not in user_ids

    def test_correct_album_titles(self, platform: StreamingPlatform) -> None:
        from streaming.sessions import ListeningSession
        user=platform.get_user("u2")
        t1=platform.get_track("t1")
        t2=platform.get_track("t2")
        t3=platform.get_track("t3")
        platform.record_session(ListeningSession("s1",user,t1,RECENT,180))
        platform.record_session(ListeningSession("s2",user,t2,RECENT,210))
        platform.record_session(ListeningSession("s3",user,t3,RECENT,195))
        result=platform.users_who_completed_albums()
        assert result[0][0].user_id == "u2"
        assert result[0][1]==["Digital Dreams"]
