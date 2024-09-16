import os
import rich_click as click
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
def find_duplicates_cli(directory: click.Path):
    """
    Recursively search for duplicate MP3 songs in the specified DIRECTORY based on metadata.
    """
    directory_str: str = str(directory)
    print(f"Scanning directory: {directory_str}...")
    duplicates: dict = find_duplicates(directory_str)
    display_duplicates(duplicates)


def get_audio_metadata(file_path: str):
    """Extracts metadata from an audio file using mutagen."""

    try:
        audio: MP3 = MP3(file_path, ID3=EasyID3)

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


def find_duplicates(directory: str) -> dict:
    """Recursively finds duplicate songs based on metadata."""
    duplicates = defaultdict(list)
    total_files = 0

    # Collect all MP3 files and process them with tqdm progress bar
    mp3_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))

    # Traverse the directory and gather duplicates
    with tqdm(total=len(mp3_files), desc="Scanning files", unit="file") as pbar:
        for file_path in mp3_files:
            total_files += 1
            metadata = get_audio_metadata(file_path)

            if metadata:
                key = (
                    metadata["title"],
                    metadata["artist"],
                    metadata["album"],
                    metadata["duration"],
                )
                duplicates[key].append(file_path)

            # Update progress bar
            pbar.update(1)

    # Filter out entries with no duplicates
    duplicate_songs = {
        key: paths for key, paths in duplicates.items() if len(paths) > 1
    }

    return duplicate_songs


def display_duplicates(duplicate_songs: dict):
    """Displays the found duplicate songs and prompts for action."""
    if not duplicate_songs:
        print("No duplicates found.")
    else:
        print("Duplicate songs found:")
        for key, paths in duplicate_songs.items():
            title, artist, album, duration = key
            print(
                "\nFiles metadata:"
                f"\nTitle: {title}, Artist: {artist}, Album: {album}, Duration: {duration} seconds"
            )
            for i, path in enumerate(paths):
                print(f" [{i+1}] {path}")

            action = click.prompt(
                "\nDo you want to delete any of these files? (y/N)", default="N"
            )
            if action == "y":
                delete_file(paths)


def delete_file(paths):
    """Prompts the user to delete one of the duplicate files."""
    while True:
        try:
            choice = click.prompt(
                f"Enter the number of the file to delete (1-{len(paths)}) or 0 to skip: ",
                type=int,
            )
            if 0 < choice <= len(paths):
                file_to_delete = paths[choice - 1]
                os.remove(file_to_delete)
                print(f"Deleted: {file_to_delete}")
                break
            elif choice == 0:
                print("Skipping deletion.")
                break
            else:
                print(
                    f"Invalid choice. Please select a number between 1 and {len(paths)}."
                )
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    find_duplicates_cli()
