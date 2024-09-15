import os
import rich_click as click
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from collections import defaultdict


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
def find_duplicates_cli(directory):
    """
    Recursively search for duplicate MP3 songs in the specified DIRECTORY based on metadata.
    """
    duplicates = find_duplicates(directory)
    display_duplicates(duplicates)


def get_audio_metadata(file_path):
    """Extracts metadata from an audio file using mutagen."""
    try:
        audio = MP3(file_path, ID3=EasyID3)
        metadata = {
            "title": audio.get("title", ["Unknown Title"])[0],
            "artist": audio.get("artist", ["Unknown Artist"])[0],
            "album": audio.get("album", ["Unknown Album"])[0],
            "duration": int(audio.info.length),
        }
        return metadata
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def find_duplicates(directory):
    """Recursively finds duplicate songs based on metadata."""
    duplicates = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                metadata = get_audio_metadata(file_path)

                if metadata:
                    key = (
                        metadata["title"],
                        metadata["artist"],
                        metadata["album"],
                        metadata["duration"],
                    )
                    duplicates[key].append(file_path)

    # Filter out entries with no duplicates
    duplicate_songs = {
        key: paths for key, paths in duplicates.items() if len(paths) > 1
    }

    return duplicate_songs


def display_duplicates(duplicate_songs):
    """Displays the found duplicate songs."""
    if not duplicate_songs:
        print("No duplicates found.")
    else:
        print("Duplicate songs found:")
        for key, paths in duplicate_songs.items():
            title, artist, album, duration = key
            print(
                f"\nTitle: {title}, Artist: {artist}, Album: {album}, Duration: {duration} seconds"
            )
            for path in paths:
                print(f" - {path}")


if __name__ == "__main__":
    find_duplicates_cli()
