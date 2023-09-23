from concurrent.futures import ThreadPoolExecutor, as_completed

from classes import Song, MusicApi
from utils import logger, possibility, similarity


class Mapper:
    """API to download songs"""

    @staticmethod
    def map_song_ids_sync(songs: list[Song], api: MusicApi) -> dict[str, list[str]]:
        """Maps yt music song ids to possible deezer ids sync"""
        mapped: dict[str, list[str]] = {}

        for index, song in enumerate(songs):
            og_id, mapped_ids = Mapper.map_song_id(song, index + 1, api)
            mapped[og_id] = mapped_ids
        return mapped

    @staticmethod
    def map_song_ids_async(
        songs: list[Song], api: MusicApi, workers: int = 2
    ) -> dict[str, list[str]]:
        """Maps yt music song ids to possible deezer ids sync"""

        mapped: dict[str, list[str]] = {}
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_mappings = {
                executor.submit(Mapper.map_song_id, song, index + 1, api): (index, song)
                for (index, song) in enumerate(songs)
            }
            for future in as_completed(future_mappings):
                url = future_mappings[future]
                try:
                    song_id, mapped_ids = future.result()
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                else:
                    mapped[song_id] = mapped_ids
        return mapped

    @staticmethod
    def map_song_id(song: Song, index: int, api: MusicApi) -> tuple[str, list[str]]:
        """Maps yt music song id to possible deezer ids"""
        song = possibility.format_song(song)
        names = possibility.get_possible_names(song)

        indent = f"{logger.indent(2)}{' ' * len(str(index))}- "

        all_candidates: set[Song] = set()
        best_candidates = similarity.SimilarSongs(song)
        for name in names:
            try:
                new_candidates = api.search_by_attributes(name)
                all_candidates.update(
                    [possibility.format_song(s) for s in new_candidates]
                )
            except Exception as exc:
                logger.log_error(f"{index}: Failed {song.pretty()}: {exc}")

            for author in song.authors:
                try:
                    new_candidates = api.search_by_attributes(name, author=author)
                    all_candidates.update(
                        [possibility.format_song(s) for s in new_candidates]
                    )
                except Exception as exc:
                    logger.log_error(f"{index}: Failed {song.pretty()}: {exc}")

            best_candidates = similarity.find_best(song, list(all_candidates))
            if len(best_candidates.identical) > 0:
                break

        if len(best_candidates.identical) > 0:
            best = next(iter(best_candidates.identical))

            log = f"{index}: Found {song.pretty()}\n" + f"{indent}{best.pretty()}"

            out_of_number = len(best_candidates.identical)

            if out_of_number > 1:
                log += f" (out of {out_of_number})"

            logger.log_success(log)
            return (song.id, [best.id])

        if len(best_candidates.similar) > 0:
            similar = list(best_candidates.similar)
            logger.log_warning(
                f"{index}: Found {song.pretty()} ({len(similar)} similar)"
            )
            subset = similar[0 : min(5, len(similar))]
            for find in subset:
                logger.log_warning(f"{indent}{find.pretty()}")

            return (song.id, [s.id for s in similar])

        if len(best_candidates.others) > 0:
            others = list(best_candidates.others)
            logger.log_error(f"{index}: Lost  {song.pretty()} ({len(others)} other)")
            subset = others[0 : min(5, len(others))]
            for find in subset:
                logger.log_error(f"{indent}{find.pretty()}")
        else:
            logger.log_error(f"{index}: Lost  {song.pretty()}")

        return (song.id, [])
