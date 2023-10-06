from abc import ABC, abstractmethod

from .song import Song
from .playlist import Playlist


class MusicApi(ABC):
    """An abstract base class for any music api"""

    @property
    def name(self) -> str:
        """Retunrs the name of the api"""
        raise NotImplementedError("Property 'name' is not implemented")

    @abstractmethod
    def search_song(self, song: Song) -> list[Song]:
        """Searches using songs name/author/other attributes"""
        raise NotImplementedError("Method 'search_by_attributes' is not implemented")

    @abstractmethod
    def search_song_id(self, song_id: str) -> Song | None:
        """Finds a track using its id"""
        raise NotImplementedError("Method 'search_song_id' is not implemented")

    @abstractmethod
    def get_user_playlists(self) -> list[Playlist]:
        """Returns user playlists"""
        raise NotImplementedError("Method 'get_user_playlists' is not implemented")
