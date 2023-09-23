from api import YTMusicApi, DeezerApi, Mapper
from utils import logger, filemanager


def main() -> None:
    """Main function"""

    yt_music_api = YTMusicApi("browser.json")
    deezer_api = DeezerApi()

    playlists = yt_music_api.get_library_playlists()

    chosen_playlist_name = "All"
    chosen_playlist = next(
        (p for p in playlists if p.name == chosen_playlist_name), None
    )
    if chosen_playlist is None:
        logger.log_error(f"Can't find playlist with name: {chosen_playlist_name}")
        logger.log_error("Available playlists are: ")
        logger.log_error(logger.pretty_list(playlists))
        return

    mapped = Mapper.map_song_ids_async(chosen_playlist.songs, deezer_api)

    valid = len([x for x in mapped if len(mapped[x]) > 0])
    logger.log_success(f"Found {valid} of {len(mapped)}")
    filemanager.create_json_file("export.json", mapped)


if __name__ == "__main__":
    main()
