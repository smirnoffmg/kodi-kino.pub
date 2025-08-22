#!/usr/bin/env python3
"""
Test Configuration for Kino.pub Kodi Addon
==========================================

This file provides test fixtures and configuration for testing the Kino.pub addon
outside of a Kodi environment using Kodistubs.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add the lib directory to the Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

# Import Kodistubs to provide Kodi module stubs
try:
    import codequick
    import xbmcaddon
    import xbmcgui
    import xbmcplugin
    import xbmcvfs
except ImportError:
    # If Kodistubs is not available, create basic mocks
    class MockAddon:
        def __init__(self):
            self.settings = {}

        def getSetting(self, setting_id: str) -> str:
            return self.settings.get(setting_id, "")

        def setSetting(self, setting_id: str, value: str):
            self.settings[setting_id] = value

        def getLocalizedString(self, string_id: int) -> str:
            return f"String {string_id}"

        def getAddonInfo(self, info_type: str) -> str:
            if info_type == "profile":
                return str(Path(__file__).parent / "test_profile")
            return ""

        def openSettings(self):
            pass

    class MockListItem:
        def __init__(self):
            self.art = {}
            self.info = {}
            self.properties = {}
            self.context_menu = []

        def setArt(self, art_dict):
            self.art.update(art_dict)

        def setInfo(self, info_type, info_dict):
            self.info.update(info_dict)

        def setProperty(self, key, value):
            self.properties[key] = value

        def addContextMenuItems(self, items):
            self.context_menu.extend(items)

    class MockDialog:
        def ok(self, heading, line1, line2="", line3=""):
            return True

        def yesno(self, heading, line1, line2="", line3="", nolabel="", yeslabel=""):
            return True

        def input(self, heading, default="", type_=1):
            return "test_input"

    class MockDialogProgress:
        def create(self, heading, line1="", line2="", line3=""):
            pass

        def update(self, percent, line1="", line2="", line3=""):
            pass

        def close(self):
            pass

    # Create mock modules
    mock_xbmcaddon = MagicMock()
    mock_xbmcaddon.Addon.return_value = MockAddon()

    mock_xbmcvfs = MagicMock()
    mock_xbmcvfs.translatePath.return_value = str(
        Path(__file__).parent / "test_profile"
    )

    mock_xbmcgui = MagicMock()
    mock_xbmcgui.ListItem.side_effect = MockListItem
    mock_xbmcgui.Dialog.return_value = MockDialog()
    mock_xbmcgui.DialogProgress.return_value = MockDialogProgress()

    mock_xbmcplugin = MagicMock()

    mock_codequick = MagicMock()
    mock_codequick.route.side_effect = lambda x: x
    mock_codequick.listitem = MagicMock()

    # Replace modules in sys.modules
    sys.modules["xbmcaddon"] = mock_xbmcaddon
    sys.modules["xbmcvfs"] = mock_xbmcvfs
    sys.modules["xbmcgui"] = mock_xbmcgui
    sys.modules["xbmcplugin"] = mock_xbmcplugin
    sys.modules["codequick"] = mock_codequick


@pytest.fixture(scope="session")
def test_profile_dir():
    """Create a temporary test profile directory"""
    profile_dir = Path(__file__).parent / "test_profile"
    profile_dir.mkdir(exist_ok=True)
    yield profile_dir
    # Cleanup is handled by the test framework


@pytest.fixture
def mock_api_response():
    """Mock API response data for testing"""
    return {
        "items": [
            {
                "id": "123",
                "title": "Test Movie",
                "type": "movie",
                "year": 2024,
                "plot": "A test movie for testing",
                "genre": ["Action", "Adventure"],
                "director": "Test Director",
                "cast": ["Actor 1", "Actor 2"],
                "duration": 120,
                "rating": 8.5,
                "mpaa": "PG-13",
                "poster": "https://example.com/poster.jpg",
                "fanart": "https://example.com/fanart.jpg",
            }
        ],
        "pagination": {"page": 1, "perpage": 10, "total": 1},
    }


@pytest.fixture
def mock_auth_response():
    """Mock authentication response data"""
    return {
        "code": "test_device_code",
        "user_code": "TEST123",
        "verification_uri": "https://kino.pub/device",
        "expires_in": 600,
        "interval": 5,
    }


@pytest.fixture
def mock_token_response():
    """Mock token response data"""
    return {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer",
    }
