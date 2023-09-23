from classes import Item
from utils import assert_parameter


class Song(Item):
    """Represents a song"""

    _duration: int | None = None
    _album: str | None = None

    def __init__(
        self,
        song_id: str,
        name: str,
        authors: list[str],
        duration: int | None = None,
        album: str | None = None,
    ) -> None:
        super().__init__(song_id, name, authors)
        if duration is not None:
            self.duration = duration
        if album is not None:
            self.album = album

    @property
    def duration(self) -> int | None:
        """Returns song's duration"""
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        assert_parameter(value, int, "duration.value")
        self._duration = value

    @property
    def album(self) -> str | None:
        """Retunrs song's album"""
        return self._album

    @album.setter
    def album(self, value: str) -> None:
        assert_parameter(value, str, "album.value")
        self._album = value

    def pretty(self) -> str:
        """Returns a pretty print"""
        base = f"SONG - '{self.name}' by {', '.join(self.authors)}"
        if self.duration is not None:
            mins, secs = divmod(self.duration, 60)
            base += f" ({mins:02d}:{secs:02d})"
        return base

    def __str__(self) -> str:
        return f"SONG - id: {self.id} | name: {self.name} | authors: {self.authors}"
