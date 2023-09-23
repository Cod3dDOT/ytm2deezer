from abc import ABC, abstractmethod

from .song import Song


class MusicApi(ABC):
    """An abstract base class for any music api"""

    @property
    def name(self) -> str:
        """Retunrs the name of the api"""
        raise NotImplementedError("property 'name' is not implemented")

    @abstractmethod
    def search_by_attributes(
        self,
        name: str,
        author: str | None = None,
        year: int | None = None,
        album: str | None = None,
        duration: int | None = None,
    ) -> list[Song]:
        """Searches using songs name/author/other attributes"""
        raise NotImplementedError("method 'search_by_attributes' is not implemented")

    @abstractmethod
    def find_by_id(self, song_id: str) -> Song | None:
        """Finds a track using its id"""
        raise NotImplementedError("method 'find_by_id' is not implemented")
