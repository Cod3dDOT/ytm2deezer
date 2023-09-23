import deezer

from classes import Song, MusicApi
from utils import logger


class DeezerApiException(Exception):
    """A simple deezer exception"""


class DeezerApiConverter:
    """A helper class for parsing"""

    @staticmethod
    def song_from_track(track: deezer.Track) -> Song:
        """Converts deezer.Track into a Song"""

        artist = track.artist.name
        if isinstance(artist, str):
            artist = [artist]
        elif not isinstance(artist, list):
            raise DeezerApiException()

        return Song(
            str(track.id),
            track.title,
            artist,
            track.duration,
            track.album.title,
        )


class DeezerApi(MusicApi):
    """Wraps deezer api"""

    _client: deezer.Client

    def __init__(self) -> None:
        super().__init__()
        self._client = deezer.Client()

    @property
    def name(self) -> str:
        return "Deezer"

    def search_by_attributes(
        self,
        name: str,
        author: str | None = None,
        year: int | None = None,
        album: str | None = None,
        duration: int | None = None,
    ) -> list[Song]:
        """Search for a song based on name/author"""
        songs: set[Song] = set()

        result = self.get_client().search(name, artist=author)
        for entry in result:
            parsed = DeezerApiConverter.song_from_track(entry)
            if parsed is not None:
                songs.add(parsed)
            else:
                logger.log_warning(f"Failed getting {entry.title}")

        return list(songs)

    def find_by_id(self, song_id: str) -> Song | None:
        int_id = int(song_id)
        result = self.get_client().get_track(int_id)
        return DeezerApiConverter.song_from_track(result)

    def get_client(self) -> deezer.Client:
        """Returns underlying client"""
        return self._client
