from concurrent.futures import ThreadPoolExecutor, as_completed

from classes import Song, MusicApi
from utils import logger, possibility, similarity


def find_songs_sync(songs: list[Song], api: MusicApi) -> dict[str, list[Song]]:
    """Finds songs in an api"""
    mapped: dict[str, list[Song]] = {}
    for index, song in enumerate(songs):
        try:
            song_id, found_songs = find_song(song, index + 1, api)
        except Exception as exc:
            print(f"{song} generated an exception: {exc}")
        else:
            mapped[song_id] = found_songs
    return mapped


def find_songs_async(
    songs: list[Song], api: MusicApi, workers: int = 2
) -> dict[str, list[Song]]:
    """Finds songs in an api async"""
    mapped: dict[str, list[Song]] = {}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_mappings = {
            executor.submit(find_song, song, index + 1, api): (index, song)
            for (index, song) in enumerate(songs)
        }
        for future in as_completed(future_mappings):
            url = future_mappings[future]
            try:
                song_id, found_songs = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
            else:
                mapped[song_id] = found_songs
    return mapped


def find_song(song: Song, index: int, api: MusicApi) -> tuple[str, list[Song]]:
    """Finds a song in an api"""
    song = possibility.format_song(song)
    names = possibility.get_possible_names(song)
    all_candidates: set[Song] = set()
    best_candidates = similarity.SimilarSongs(song)

    for new_name in names:
        try:
            new_candidates = api.search_song(
                Song(song.id, new_name, song.authors, song.duration, song.album)
            )
            all_candidates.update([possibility.format_song(s) for s in new_candidates])
        except Exception as exc:
            logger.log_error(f"{index}: Failed {song.pretty()}: {exc}")

        best_candidates = similarity.find_best(song, list(all_candidates))
        if len(best_candidates.identical) > 0:
            break

    return select_best(best_candidates, index)


def select_best(finds: similarity.SimilarSongs, index: int) -> tuple[str, list[Song]]:
    indent = f"{logger.indent(2)}{' ' * len(str(index))}- "

    if len(finds.identical) > 0:
        best = next(iter(finds.identical))
        log = (
            f"{index}: Found {finds.song.pretty()}\n"
            + f"{indent}{best.pretty()}  (out of {len(finds.identical)})"
        )
        logger.log_success(log)
        return (finds.song.id, [best])

    if len(finds.similar) > 0:
        similar = list(finds.similar)
        logger.log_warning(
            f"{index}: Found {finds.song.pretty()} ({len(similar)} similar)"
        )
        subset = similar[0 : min(5, len(similar))]
        for find in subset:
            logger.log_warning(f"{indent}{find.pretty()}")
        return (finds.song.id, similar)

    if len(finds.others) > 0:
        others = list(finds.others)
        # return (song.id, others)
        logger.log_error(f"{index}: Lost  {finds.song.pretty()} ({len(others)} other)")
        subset = others[0 : min(5, len(others))]
        for find in subset:
            logger.log_error(f"{indent}{find.pretty()}")
    else:
        logger.log_error(f"{index}: Lost  {finds.song.pretty()}")

    return (finds.song.id, [])
