import re

from classes import Song


def get_possible_names(song: Song) -> list[str]:
    """Retunrs possible name combinations for a song"""
    name = song.name.replace(")(", ") (").strip()
    names: set[str] = set([name])
    additions: set[str] = set()
    while "(" in name and ")" in name:
        addition = name[name.find(" (") : name.find(")") + 1]
        name = name.replace(addition, "")
        additions.add(addition)
    names.add(name)
    for add in additions:
        names.add(name + add)
    return list(names)


def format_song(song: Song) -> Song:
    """Formats song"""
    with_name = format_song_name(song)
    with_authors = format_song_authors(with_name)
    return with_authors


def format_song_authors(song: Song) -> Song:
    """Ads (feat author) to songs authors"""
    new_authors: set[str] = set()
    feat_regex = r"\s*(?:\((?:ft|featuring|feat)\.?\s*(.*)\))"
    match = re.search(feat_regex, song.name)
    if match:
        new_authors.add(match.groups()[0])
    video_format_regex = r"(.*?)\s+-\s+(.+)"
    match = re.search(video_format_regex, song.name)
    if match:
        new_authors.add(match.groups()[0])
    for author in set(song.authors):
        if " & " in author:
            new_authors.update(author.split(" & "))
        if " / " in author:
            new_authors.update(author.split(" / "))
    new_authors_list = list(new_authors)
    new_authors_list[0:0] = song.authors
    return Song(song.id, song.name, new_authors_list, song.duration, song.album)


def format_song_name(song: Song) -> Song:
    name = song.name
    delete = [
        " (Lyrics)",
        " (Official Video)",
        " (Visualization)",
        " (Music Visualization)",
    ]
    for d in delete:
        name = name.replace(d, "")
    video_format_regex = r"(.*?)\s+-\s+(.+)"
    match = re.search(video_format_regex, name)
    if match:
        name = match.groups()[1]
    return Song(song.id, name, song.authors, song.duration, song.album)
