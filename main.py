from api import YTMusicApi, DeezerApi, find_songs_async
from utils import logger, filemanager
from classes import MusicApi


def main() -> None:
    """Main function"""
    yt_music_api = YTMusicApi("oauth.json")
    deezer_api = DeezerApi()
    # convert_playlist("All Them Moods", yt_music_api, deezer_api)
    deezer_add("All Them Moods", deezer_api)


def convert_playlist(pl_name: str, from_api: MusicApi, to_api: MusicApi) -> None:
    """Converts playlist from one platform to another"""
    playlists = from_api.get_user_playlists()
    chosen_playlist = next((p for p in playlists if p.name == pl_name), None)

    if chosen_playlist is None:
        logger.log_error(f"Can't find playlist with name: {pl_name}")
        logger.log_error("Available playlists are: ")
        logger.log_error(logger.pretty_list(playlists))
        return

    mapped = find_songs_async(chosen_playlist.songs, to_api)

    valid = len([x for x in mapped if len(mapped[x]) > 0])
    logger.log_success(f"Found {valid} of {len(mapped)}")
    filemanager.create_json_file(
        "export.json",
        {og_id: [s.id for s in songs] for (og_id, songs) in mapped.items()},
    )


def deezer_add(pl_name: str, to_api: DeezerApi) -> None:
    export = filemanager.read_json_file("export.json")
    for key, val in export.items():
        if len(val) != 1:
            logger.log_error(f"Skipping track: {key}")
            continue

        print(to_api.add_song_by_id(val[0]))


if __name__ == "__main__":
    main()
