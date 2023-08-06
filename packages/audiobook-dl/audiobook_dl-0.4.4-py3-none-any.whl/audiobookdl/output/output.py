from audiobookdl import logging

import os
import platform
from typing import List, Dict
import subprocess

LOCATION_DEFAULTS = {
    'album': 'NA',
    'artist': 'NA',
}

def gen_output_filename(booktitle: str, file: Dict[str, str], template: str) -> str:
    """Generates an output filename based on different attributes of the
    file"""
    arguments = {**file, **{"booktitle": booktitle}}
    filename = template.format(**arguments)
    return _fix_output(filename)


def combine_audiofiles(filenames: List[str], tmp_dir: str, output_path: str):
    """Combines the given audiofiles in `path` into a new file"""
    inputs = "|".join(filenames)
    subprocess.run(
        ["ffmpeg", "-i", f"concat:{inputs}", "-safe", "0", "-c", "copy", output_path],
        capture_output=not logging.ffmpeg_output,
    )


def convert_output(filenames: List[str], output_format: str):
    """Converts a list of audio files into another format and return new
    files"""
    new_paths = []
    for old_path in filenames:
        split_path = os.path.splitext(old_path)
        new_path = f"{split_path[0]}.{output_format}"
        if not output_format == split_path[1][1:]:
            subprocess.run(
                ["ffmpeg", "-i", old_path, new_path],
                capture_output=not logging.ffmpeg_output)
            os.remove(old_path)
        new_paths.append(f"{os.path.splitext(old_path)[0]}.{output_format}")
    return new_paths


def gen_output_location(template: str, metadata: Dict[str, str], remove_chars: str) -> str:
    """Generates the location of the output based on attributes of the
    audiobook"""
    if metadata is None:
        metadata = {}
    metadata["title"] = _fix_output(metadata["title"])
    metadata = {**LOCATION_DEFAULTS, **metadata}
    formatted = template.format(**metadata)
    formatted = _remove_chars(formatted, remove_chars)
    return formatted


def _fix_output(title: str) -> str:
    """Returns title without characters system can't handle"""
    title = title.replace("/", "-")
    if platform.system() == "Windows":
        title = _remove_chars(title, ':*\\?<>|"\'’')
    return title


def _remove_chars(s: str, chars: str) -> str:
    """Removes `chars` from `s`"""
    for i in chars:
        s = s.replace(i, "")
    return s
