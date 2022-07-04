"""Simulate a local cache for remote files.

Tools like DataCorral download files from the cloud on demand.
If there's already a local copy of the file, DC re-uses that
rather than downloading the file again.

`FileCache` simulates this by "downloading" (copying) files
from one local directory to another.  When a caller asks for
a file called "tammy.csv", `FileCache` downloads the file if
its name isn't already in the cache, then returns the path
to the local copy of the file.

Things to change:

1.  Download from URLs using the `requests` library.
2.  Make `FileCache` configurable so that a caller can specify
    a base URL for remote files and the local cache directory
    (but only has to specify them once). - done
3.  Make `FileCache` able to download both remote files and
    local files.
4.  Check that files whose names are in the cache are actually
    stored locally rather than trusting the cache.
5.  Rebuild the cache from the files that we already have on
    disk, and explain why this is both useful and dangerous.
6.  Explain why we need to be able to clear the cache. (Hint:
    think about testing.)
7.  Discuss why `get` and `clear` are `classmethod` rather than
    `staticmethod`.  # because depends on the cache path?
"""

import csv
import filecmp
import requests
import shutil
import validators

from pathlib import Path
from urllib.parse import urljoin


CONFIG = {
    "cache": Path(__file__).parent.parent.joinpath("cache"),
    "remote": Path(__file__).parent.parent.joinpath("remote"),
}

# Arbitrary limit of 250MB - change as needed
DOWNLOAD_LIMIT = 2.5e8

CACHE_INDEX = "cache_index.csv"
CACHE_HEADER = ["cache_path", "remote_path"]


class FileCache:
    """Cache large remote files."""

    def __init__(self, cache_dir=None, remote_url=None):
        if cache_dir:
            self.cache_dir = cache_dir
        else:
            self.cache_dir = CONFIG["cache"]

        if remote_url:
            self.remote_url = remote_url
        else:
            self.remote_url = CONFIG["remote"]

        self.cache_index = Path(self.cache_dir, CACHE_INDEX)
        self.setup_cache()

    def get(self, requested_file):
        """Return path to cached copy of file, getting as needed."""

        # special handling of URLs
        if validators.url(requested_file):
            # extact filename from URL as that'll be how it's saved in the cache that we need to check
            extracted_filename = Path(requested_file).name
            cache_path = Path(self.cache_dir, extracted_filename)
            remote_path = requested_file
        else:
            cache_path = Path(self.cache_dir, requested_file)
            remote_path = Path(self.remote_url, requested_file)

        # first check if file is in the cache
        if cache_path.exists():
            # confirm that it's in the cache index and if not then add it
            if not self.check_if_in_cache(cache_path):
                self.add_to_cache_index(remote_path, cache_path)
        else:
            if validators.url(requested_file):
                self._download_file(requested_file, cache_path)
            else:
                self.handle_local_file(requested_file, cache_path)

        return str(cache_path)

    def clear(self):
        """Clear the cache, deleting local files."""
        for filename in self.cache_dir.iterdir():
            filename.unlink()
        self.setup_cache()

    def _get_file(self, remote_path, local_path):
        """Simulate getting a remote file."""
        remote_path = Path(self.remote_url, remote_path)
        if not remote_path.exists():
            raise ValueError(f"{remote_path} does not exist")
        shutil.copyfile(remote_path, local_path)

    def _download_file(self, remote_url, local_path):
        """Downloads a file from a remote url"""
        h = requests.head(remote_url, allow_redirects=True)
        header = h.headers
        content_length = header.get("content-length", None)  # this is case insensitive
        if content_length is None:
            raise RuntimeError(
                f"Cannot validate the size of the requested file: {remote_url}. Not downloading."
            )
        elif content_length and content_length > DOWNLOAD_LIMIT:  # this is in bytes
            raise RuntimeError(f"{remote_url} is too large (> {DOWNLOAD_LIMIT} bytes).")
        r = requests.get(remote_url, allow_redirects=True)
        if r.status_code == 200:
            with open(local_path, "wb") as fhandle:
                fhandle.write(r.content)
            self.add_to_cache_index(remote_url, local_path)
        else:
            raise RuntimeError(f"{remote_url} could not be downloaded.")

    def handle_local_file(self, requested_file, cache_path):
        """Processes a file requested from a local directory"""
        self._get_file(requested_file, cache_path)
        remote_path = Path(self.remote_url, requested_file)
        self.add_to_cache_index(remote_path, cache_path)

    def setup_cache(self):
        """Creates an index for the cache if it doesn't exist"""
        if not Path(self.cache_index).exists():
            with open(self.cache_index, "w") as fhandle:
                writer = csv.DictWriter(fhandle, fieldnames=CACHE_HEADER)
                writer.writeheader()

    def check_if_in_cache(self, local_path):
        """Checks if a file is in the cache index"""
        with open(self.cache_index, "r") as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                if row[CACHE_HEADER[0]] == local_path:
                    return True
        return False

    def add_to_cache_index(self, remote_path, local_path):
        """Adds a file to the cache index"""
        with open(self.cache_index, "a") as fhandle:
            writer = csv.DictWriter(fhandle, fieldnames=CACHE_HEADER)
            writer.writerow(
                {
                    CACHE_HEADER[0]: local_path,
                    CACHE_HEADER[1]: remote_path,
                }
            )
