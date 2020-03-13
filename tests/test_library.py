import unittest

from mopidy.models import Image, Ref
from mopidy_gmusic import backend as backend_lib

from tests.test_extension import ExtensionTest


class LibraryTest(unittest.TestCase):
    def setUp(self):
        config = ExtensionTest.get_config()
        self.backend = backend_lib.GMusicBackend(config=config, audio=None)

    def test_browse_radio_deactivated(self):
        config = ExtensionTest.get_config()
        config["gmusic"]["radio_stations_in_browse"] = False
        self.backend = backend_lib.GMusicBackend(config=config, audio=None)

        refs = self.backend.library.browse("gmusic:directory")
        for ref in refs:
            assert ref.uri != "gmusic:radio"

    def test_browse_none(self):
        refs = self.backend.library.browse(None)
        assert refs == []

    def test_browse_invalid(self):
        refs = self.backend.library.browse("gmusic:invalid_uri")
        assert refs == []

    def test_browse_root(self):
        refs = self.backend.library.browse("gmusic:directory")
        found = False
        for ref in refs:
            if ref.uri == "gmusic:album":
                found = True
                break
        assert found, "ref 'gmusic:album' not found"
        found = False
        for ref in refs:
            if ref.uri == "gmusic:artist":
                found = True
                break
        assert found, "ref 'gmusic:artist' not found"
        found = False
        for ref in refs:
            if ref.uri == "gmusic:track":
                found = True
                break
        assert found, "ref 'gmusic:track' not found"
        found = False
        for ref in refs:
            if ref.uri == "gmusic:radio":
                found = True
                break
        assert found, "ref 'gmusic:radio' not found"

    def test_browse_tracks(self):
        refs = self.backend.library.browse("gmusic:track")
        assert refs is not None

    def test_browse_artist(self):
        refs = self.backend.library.browse("gmusic:artist")
        assert refs is not None

    def test_browse_artist_id_invalid(self):
        refs = self.backend.library.browse("gmusic:artist:artist_id")
        assert refs is not None
        assert refs == []

    def test_browse_album(self):
        refs = self.backend.library.browse("gmusic:album")
        assert refs is not None

    def test_browse_album_id_invalid(self):
        refs = self.backend.library.browse("gmusic:album:album_id")
        assert refs is not None
        assert refs == []

    def test_browse_radio(self):
        refs = self.backend.library.browse("gmusic:radio")
        # tests should be unable to fetch stations :(
        assert refs is not None
        assert refs == [
            Ref.directory(uri="gmusic:radio:IFL", name="I'm Feeling Lucky")
        ]

    def test_browse_station(self):
        refs = self.backend.library.browse("gmusic:radio:invalid_stations_id")
        # tests should be unable to fetch stations :(
        assert refs == []

    def test_lookup_invalid(self):
        refs = self.backend.library.lookup("gmusic:invalid_uri")
        # tests should be unable to fetch any content :(
        assert refs == []

    def test_lookup_invalid_album(self):
        refs = self.backend.library.lookup("gmusic:album:invalid_uri")
        # tests should be unable to fetch any content :(
        assert refs == []

    def test_lookup_invalid_artist(self):
        refs = self.backend.library.lookup("gmusic:artis:invalid_uri")
        # tests should be unable to fetch any content :(
        assert refs == []

    def test_lookup_invalid_track(self):
        refs = self.backend.library.lookup("gmusic:track:invalid_uri")
        # tests should be unable to fetch any content :(
        assert refs == []

    def test_search(self):
        refs = self.backend.library.search({"artist": ["abba"]})
        assert refs is not None

    def test_get_images_unknown_uri(self):
        refs = self.backend.library.get_images(["gmusic:track:unknown_uri"])
        assert refs == {"gmusic:track:unknown_uri": []}

    def test_get_images_known_uris(self):
        self.backend.library.images = {
            "gmusic:track:89bbf2f8-5f98-3108-a29d-b1c5e2c671a2": [
                Image(uri="https://cdn.com/image1.jpg")
            ],
            "gmusic:track:fd6f9d17-63d5-3d45-b2d2-efbb5cdd4be5": [
                Image(uri="https://cdn.com/image2.jpg")
            ],
            "gmusic:track:89a7bd77-3d99-3ad4-a6f6-7b9d025f02a8": [
                Image(uri="https://cdn.com/image3.jpg")
            ],
            "gmusic:track:6a89747a-c2f9-3815-a8e4-6c95ebe6c083": [
                Image(uri="https://cdn.com/image4.jpg")
            ],
            "gmusic:track:21535e0f-2583-3e66-9766-b0f6e180c6b0": [
                Image(uri="https://cdn.com/image5.jpg")
            ],
        }
        refs = self.backend.library.get_images(
            [
                "gmusic:track:fd6f9d17-63d5-3d45-b2d2-efbb5cdd4be5",
                "gmusic:track:89a7bd77-3d99-3ad4-a6f6-7b9d025f02a8",
                "gmusic:track:21535e0f-2583-3e66-9766-b0f6e180c6b0",
            ]
        )
        assert refs == {
            "gmusic:track:fd6f9d17-63d5-3d45-b2d2-efbb5cdd4be5": [
                Image(uri="https://cdn.com/image2.jpg")
            ],
            "gmusic:track:89a7bd77-3d99-3ad4-a6f6-7b9d025f02a8": [
                Image(uri="https://cdn.com/image3.jpg")
            ],
            "gmusic:track:21535e0f-2583-3e66-9766-b0f6e180c6b0": [
                Image(uri="https://cdn.com/image5.jpg")
            ],
        }
