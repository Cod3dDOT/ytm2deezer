from ytmusicapi import YTMusic

from classes import Playlist, Song, MusicApi
from utils import logger


class YTMusicApiException(Exception):
    """A simple yt music exception"""


class YTMusicApiConverter:
    """A helper class for yt music json"""

    @staticmethod
    def get_title(json_dict: dict) -> str | None:
        """Returns title for song/playlist"""
        return json_dict.get("title")

    @staticmethod
    def get_duration(json_dict: dict) -> int | None:
        """Returns duration for song/playlist"""
        return json_dict.get("duration_seconds")

    @staticmethod
    def get_album_name(json_dict: dict) -> str | None:
        """Returns album name for song/playlist"""
        album_json = json_dict.get("album")
        if album_json is not None:
            return album_json.get("name")
        return None

    @staticmethod
    def get_author_names(json_dict: dict) -> list[str]:
        """Returns album name for song/playlist"""
        song_authors = json_dict.get("artists")
        playlist_authors = json_dict.get("author")

        if song_authors is not None:
            if not isinstance(song_authors, list):
                return [song_authors.get("name")]
            return [a.get("name") for a in song_authors]

        if playlist_authors is not None:
            if not isinstance(playlist_authors, list):
                return [playlist_authors.get("name")]
            return [a.get("name") for a in playlist_authors]

        return []

    @staticmethod
    def song_from_json(json_dict: dict) -> Song | None:
        """Attempts to parse a song from yt music json"""

        song_id = json_dict.get("videoId")
        name = YTMusicApiConverter.get_title(json_dict)
        authors = YTMusicApiConverter.get_author_names(json_dict)
        duration = YTMusicApiConverter.get_duration(json_dict)
        album = YTMusicApiConverter.get_album_name(json_dict)

        if song_id is None or name is None:
            return None

        return Song(song_id, name, authors, duration, album)

    @staticmethod
    def playlist_from_json(json_dict: dict) -> Playlist | None:
        """Attempts to parse a playlist from yt music json"""

        pl_id = json_dict.get("playlistId")
        name = YTMusicApiConverter.get_title(json_dict)
        authors = YTMusicApiConverter.get_author_names(json_dict)
        # duration = YTConverter.get_duration(json_dict)
        # album = YTConverter.get_album_name(json_dict)

        if pl_id is None or name is None:
            return None

        return Playlist(pl_id, name, authors)


class YTMusicApi(MusicApi):
    """Wraps ytmusic api"""

    _client: YTMusic

    def __init__(self, auth_filepath: str) -> None:
        super().__init__()
        self._client = YTMusic(auth_filepath)

    @property
    def name(self) -> str:
        return "YTMusic"

    def get_library_playlists(self) -> list[Playlist]:
        """Gtes user playlists (with songs)"""
        playlists = self.get_client().get_library_playlists()

        parsed: list[Playlist] = []
        for p_json in playlists:
            plist = YTMusicApiConverter.playlist_from_json(p_json)

            if plist is None:
                logger.log_warning(f"Skipping playlist: {p_json.get('title')}")
                continue

            # ignore liked songs playlist
            if plist.id == "LM":
                logger.log_message(f"Skipping playlist: {plist.name}")
                continue

            songs = self.get_client().get_playlist(plist.id, None, suggestions_limit=0).get("tracks")  # type: ignore

            if songs is None:
                songs = []

            for s_json in songs:
                song = YTMusicApiConverter.song_from_json(s_json)

                if song is None:
                    logger.log_warning(
                        f"Skipping song '{s_json.get('title')}' in playlist: {plist.name}"
                    )
                    continue

                plist.add_song(song)

            parsed.append(plist)

        return parsed

    def get_library_songs(self) -> list[Song]:
        """Returns songs saved in library"""
        songs = self.get_client().get_library_songs(None, False)  # type: ignore

        parsed: list[Song] = []
        for s_json in songs:
            song = YTMusicApiConverter.song_from_json(s_json)
            if song is None:
                logger.log_warning("Skipping library song")
                continue
            parsed.append(song)
        return parsed

    def get_liked_songs(self) -> list[Song]:
        """Returns liked songs"""
        songs = self.get_client().get_liked_songs(None).get("tracks")  # type: ignore

        if songs is None:
            raise YTMusicApiException()

        parsed: list[Song] = []
        for s_json in songs:
            song = YTMusicApiConverter.song_from_json(s_json)
            if song is None:
                logger.log_warning("Skipping liked song")
                continue
            parsed.append(song)
        return parsed

    def get_history_songs(self) -> list[Song]:
        """Returns recently playes songs"""
        songs = self.get_client().get_history()

        if songs is None:
            raise YTMusicApiException()

        parsed: list[Song] = []
        for s_json in songs:
            song = YTMusicApiConverter.song_from_json(s_json)
            if song is None:
                logger.log_warning("Skipping history song")
                continue
            parsed.append(song)
        return parsed

    def get_client(self) -> YTMusic:
        """Returns ytmusic client"""
        return self._client

    def search_by_attributes(
        self,
        name: str,
        author: str | None = None,
        year: int | None = None,
        album: str | None = None,
        duration: int | None = None,
    ) -> list[Song]:
        """Search for a song based on name"""
        songs: set[Song] = set()

        result = self.get_client().search(name, scope="songs")
        for entry in result:
            parsed = YTMusicApiConverter.song_from_json(entry)
            if parsed is not None:
                songs.add(parsed)
            else:
                logger.log_warning(
                    f"Failed getting {YTMusicApiConverter.get_title(entry)}"
                )

        return list(songs)

    def find_by_id(self, song_id: str) -> Song | None:
        result = self.get_client().get_song(videoId=song_id)
        return YTMusicApiConverter.song_from_json(result)
