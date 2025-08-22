#!/usr/bin/env python3
"""
Unit tests for Kino.pub API client
==================================

Tests for the KinoPubAPI class functionality.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the parent directory to the Python path to import lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.api import KinoPubAPI


class TestKinoPubAPI:
    """Test cases for KinoPubAPI class"""

    def setup_method(self):
        """Set up test fixtures"""
        with patch("lib.api.xbmcaddon.Addon"):
            with patch("lib.api.xbmcvfs"):
                self.api = KinoPubAPI()

    def test_init(self):
        """Test API initialization"""
        assert self.api.base_url == "https://api.service-kp.com"
        assert self.api.client_id == "xbmc"
        assert self.api.client_secret == "cgg3gtifu46urtfp2zp1nqtba0k2ezxh"
        assert self.api.access_token is None
        assert self.api.refresh_token is None

    def test_is_authenticated_false(self):
        """Test authentication check when not authenticated"""
        assert self.api.is_authenticated() is False

    def test_is_authenticated_true(self):
        """Test authentication check when authenticated"""
        self.api.access_token = "test_token"
        assert self.api.is_authenticated() is True

    @patch("lib.api.KinoPubAPI._make_request")
    def test_start_device_auth_success(self, mock_make_request):
        """Test successful device authentication start"""
        mock_make_request.return_value = {
            "code": "test_device_code",
            "user_code": "TEST123",
            "verification_uri": "https://kino.pub/device",
            "expires_in": 8600,
            "interval": 5,
        }

        result = self.api.start_device_auth()

        assert result is True
        assert self.api.device_code == "test_device_code"
        assert self.api.user_code == "TEST123"
        assert self.api.verification_uri == "https://kino.pub/device"
        mock_make_request.assert_called_once()

    @patch("lib.api.KinoPubAPI._make_request")
    def test_start_device_auth_failure(self, mock_make_request):
        """Test failed device authentication start"""
        mock_make_request.return_value = {}

        result = self.api.start_device_auth()

        assert result is False
        mock_make_request.assert_called_once()

    def test_get_items_params(self):
        """Test get_items method parameters"""
        self.api.access_token = "test_token"

        with patch.object(self.api, "_make_request") as mock_request:
            mock_request.return_value = {"items": []}

            self.api.get_items(page=2, perpage=10, type_filter="movie")

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["params"]["page"] == 2
            assert call_args[1]["params"]["perpage"] == 10
            assert call_args[1]["params"]["type"] == "movie"

    def test_search_content_params(self):
        """Test search_content method parameters"""
        self.api.access_token = "test_token"

        with patch.object(self.api, "_make_request") as mock_request:
            mock_request.return_value = {"items": []}

            self.api.search_content("test query", page=3, perpage=15)

            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["params"]["q"] == "test query"
            assert call_args[1]["params"]["page"] == 3
            assert call_args[1]["params"]["perpage"] == 15


if __name__ == "__main__":
    pytest.main([__file__])
