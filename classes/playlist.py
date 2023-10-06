from classes import Item, Song
from utils import assert_parameter


class Playlist(Item):
    """A class to represent yt music playlists"""

    _songs: dict[str, list[Song]] = {}

    def __init__(self, pl_id: str, name: str, authors: list[str]) -> None:
        super().__init__(pl_id, name, authors)
        self._songs = {}

    @property
    def songs(self) -> list[Song]:
        """Returns list of songs"""
        return [item for row in self._songs.values() for item in row]

    def add_song(self, song: Song, duplicate: bool = False) -> bool:
        """Adds a song to playlist"""
        assert_parameter(song, Song, "song")

        if self._songs.get(song.id) is None:
            self._songs[song.id] = [song]
            return True

        if duplicate:
            self._songs[song.id].append(song)
            return True

        return False

    def add_songs(self, songs: list[Song]) -> None:
        """Adds a list of songs"""
        for s in songs:
            self.add_song(s)

    def pretty(self) -> str:
        """Returns a pretty print"""
        return f"PLAYLIST - '{self.name}' by {' & '.join(self.authors)}"

    def __str__(self) -> str:
        return (
            f"PLAYLIST (id: {self.id} | name: {self.name} "
            + f"| authors: {self.authors} | songs: {len(self.songs)})"
        )
