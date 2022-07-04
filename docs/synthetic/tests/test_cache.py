import csv
import pytest
import os
import pyfakefs

from pathlib import Path
from unittest import mock

from dnadoh.cache import FileCache, CACHE_INDEX, CONFIG, CACHE_HEADER

TEST_FNAME = "foo.txt"


@pytest.fixture()
def cache(fs):
    for path in CONFIG.values():
        fs.create_dir(path)
    cacher = FileCache()
    return cacher


@pytest.fixture()
def non_empty_cache(fs):
    for path in CONFIG.values():
        fs.create_dir(path)

    cache = FileCache()
    fs.create_file(Path(cache.cache_dir, TEST_FNAME))
    return cache


def assert_file_in_index(cache, expected_data):
    """Utility function to check that the file is in the index.
    Only works if it's the first non header row"""
    with open(cache.cache_index, "r") as fhandle:
        data = csv.DictReader(fhandle)
        assert next(data) == expected_data


def test_init(fs):
    """Tests that the cache and remote directories are set properly"""
    cache_dir = "/some/test/dir"
    fs.create_dir(cache_dir)
    remote = "https://www.github.com"
    cache = FileCache(cache_dir, remote)
    assert cache.cache_dir == cache_dir
    assert cache.remote_url == remote
    assert Path(cache_dir, CACHE_INDEX).exists()


def test_get_when_not_in_cache(fs, cache):
    """Tests that when a file is not in the cache, that it is fetched"""
    fname = "test.txt"
    fs.create_file(Path(cache.remote_url, fname))
    cache.get(fname)
    expected = {
        CACHE_HEADER[0]: str(Path(cache.cache_dir, fname)),
        CACHE_HEADER[1]: str(Path(cache.remote_url, fname)),
    }
    assert Path(cache.cache_dir, fname).exists()
    assert_file_in_index(cache, expected)


@mock.patch.object(FileCache, "handle_local_file")
def test_get_when_cached(mock, non_empty_cache):
    """Tests that when a file is cached, it is not fetched using _get_file()"""
    cache_path = non_empty_cache.get(TEST_FNAME)
    expected = {
        CACHE_HEADER[0]: str(Path(non_empty_cache.cache_dir, TEST_FNAME)),
        CACHE_HEADER[1]: str(Path(non_empty_cache.remote_url, TEST_FNAME)),
    }
    assert mock.call_count == 0
    assert cache_path == str(Path(non_empty_cache.cache_dir, TEST_FNAME))
    assert_file_in_index(non_empty_cache, expected)


def test_in_cache_index_but_not_dir(fs, cache):
    """Tests that when a file is in the cache index, but not actually in the
    cache directory, that it is fetched"""
    fname = "fake_file.txt"
    # sabotage the index by adding to it
    with open(cache.cache_index, "a") as fhandle:
        writer = csv.DictWriter(fhandle, fieldnames=CACHE_HEADER)
        writer.writerow(
            {
                CACHE_HEADER[0]: str(Path(cache.cache_dir, fname)),
                CACHE_HEADER[1]: "/random/directory",
            }
        )
    with mock.patch.object(FileCache, "handle_local_file") as mocked_function:
        cache.get("fake_file.txt")
        assert mocked_function.call_count == 1


# not sure why this is failing now
# OSError: Could not find a suitable TLS CA certificate bundle, invalid path: /Users/tammylau/conda/envs/dnadoh_dev/lib/python3.8/site-packages/certifi/cacert.pem
@pytest.mark.skip("Failing test due to certificate issues - may be pytest related?")
def test_remote_download(cache):
    remote_file = "http://github.com/tammy-dg/tammys-simple-web-server/blob/master/test/test.png?raw=true"
    cache.get(remote_file)
    print(cache.cache_index)
    cache.clear()
