# MP3 Duplicate Finder & Manager

This Python project identifies and will eventually manage duplicate MP3 files in a specified directory based on metadata such as title, artist, album, and duration. Using the `mutagen` library, the script recursively scans a directory to locate potential duplicates.

It's also an excuse to try out `poetry`.

## Features

- Recursively search directories for MP3 files.
- Identify duplicate MP3 files based on key metadata.

## Future Features

The intent of this project is not only to find duplicates but to provide tools to help you **manage** them. Future versions may include:

- **Interactive duplicate resolution**: Options to delete, move, or rename duplicates.
- **Metadata enhancement**: Automatically fill in missing metadata (e.g., title, artist) using web services like MusicBrainz, Discogs, or other APIs to improve metadata accuracy for files lacking information.
- **Support for additional file formats**: Expand beyond `.mp3` to other audio formats like `.flac`, `.wav`, etc.

## Requirements

- Python 3.11+
- Libraries:
  - `mutagen`
  - `rich-click`

You can install the necessary dependencies using the following command:

```bash
pip install poetry
poetry install
```

## Usage
To run the script, simply provide the directory you want to search as an argument:

```bash
python duplicate_songs.py /path/to/music/folder
```

## Contributing
Very new project, not ready for contributions.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
