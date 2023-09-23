import difflib

from classes import Song
from utils import slugify


class SimilarSongs:
    _song: Song
    _identical: set[Song]
    _similar: set[Song]
    _others: set[Song]

    def __init__(self, song: Song) -> None:
        self._song = song
        self._identical = set()
        self._similar = set()
        self._others = set()

    def add_identical(self, song: Song):
        self._identical.add(song)

    def add_similar(self, song: Song):
        self._similar.add(song)

    def add_other(self, song: Song):
        self._others.add(song)

    @property
    def identical(self):
        return self._identical

    @property
    def similar(self):
        return self._similar

    @property
    def others(self):
        return self._others


def have_similar_names(left: Song, right: Song) -> bool:
    """Returns true if songs have similar authors"""
    diff = difflib.SequenceMatcher(None, left.name, right.name).ratio()
    return diff > 0.8


def have_similar_authors(left: Song, right: Song) -> bool:
    """Returns true if songs have similar authors"""
    left_set = set(left.authors)
    right_set = set(right.authors)
    diff = left_set - right_set
    if len(diff) < len(left_set):
        return True
    return False


def have_similar_duration(left: Song, right: Song) -> bool:
    """Returns True if songs have similar duration"""
    return (
        left.duration is not None
        and right.duration is not None
        and abs(left.duration - right.duration) < 3
    )


def find_best(song_og: Song, finds_og: list[Song]) -> SimilarSongs:
    """Finds best match/matches out of the list of candidates"""
    result = SimilarSongs(song_og)
    song_slug = Song(
        song_og.id,
        song_og.name,
        [slugify(a) for a in song_og.authors],
        song_og.duration,
        slugify(song_og.album),
    )
    finds_slug = [
        Song(
            s.id,
            s.name,
            [slugify(a) for a in s.authors],
            s.duration,
            slugify(s.album),
        )
        for s in finds_og
    ]
    for find_slug in finds_slug:
        if not have_similar_names(song_slug, find_slug):
            continue
        authors = have_similar_authors(song_slug, find_slug)
        duration = have_similar_duration(song_slug, find_slug)
        find_og = next(f for f in finds_og if f.id == find_slug.id)
        if authors and duration:
            result.add_identical(find_og)
        elif authors and not duration:
            result.add_similar(find_og)
        else:
            result.add_other(find_og)
    if (
        song_og.duration is None
        and len(result.identical) == 0
        and len(result.similar) <= 2
    ):
        for sim in result.similar:
            result.add_identical(sim)
    return result
