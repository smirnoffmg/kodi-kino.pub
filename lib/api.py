#!/usr/bin/env python3
"""
Kino.pub API Client
==================

API client for Kino.pub streaming service with OAuth 2.0 Device Flow authentication.
"""

import json
import os
import time
from urllib.parse import urljoin

import requests  # type: ignore[import-untyped]
import xbmcaddon  # type: ignore[import-untyped]
import xbmcvfs  # type: ignore[import-untyped]


class KinoPubAPI:
    """
    Kino.pub API Client with Device Flow Authentication

    Uses public device credentials for OAuth 2.0 Device Flow authentication.
    """

    def __init__(self) -> None:
        self.base_url = "https://api.service-kp.com"

        # Public device credentials (found in client implementations)
        self.client_id = "xbmc"
        self.client_secret = "cgg3gtifu46urtfp2zp1nqtba0k2ezxh"

        self.access_token = None
        self.refresh_token = None
        self.device_code = None
        self.user_code = None
        self.verification_uri = None
        self.expires_in = None
        self.interval = 5

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "KinoPub-Kodi-Addon/1.0",
            }
        )

        # Load cached tokens
        self._load_tokens()

    def _get_cache_path(self) -> str:
        """Get cache file path for storing tokens"""
        addon = xbmcaddon.Addon()
        profile_path = addon.getAddonInfo("profile")
        return str(xbmcvfs.translatePath(profile_path))

    def _load_tokens(self) -> None:
        """Load cached access and refresh tokens"""
        try:
            cache_path = self._get_cache_path()
            tokens_file = os.path.join(cache_path, "tokens.json")

            if xbmcvfs.exists(tokens_file):
                with open(tokens_file) as f:
                    tokens = json.load(f)
                    self.access_token = tokens.get("access_token")
                    self.refresh_token = tokens.get("refresh_token")
        except Exception:
            # Log error but continue without cached tokens
            pass

    def _save_tokens(self) -> None:
        """Save access and refresh tokens to cache"""
        try:
            cache_path = self._get_cache_path()
            os.makedirs(cache_path, exist_ok=True)
            tokens_file = os.path.join(cache_path, "tokens.json")

            tokens = {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
            }

            with open(tokens_file, "w") as f:
                json.dump(tokens, f)
        except Exception:
            # Log error but continue
            pass

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        require_auth: bool = True,
        use_json: bool = False,
    ) -> dict:
        """Make HTTP request to API with error handling"""
        url = urljoin(self.base_url, endpoint)

        # Prepare headers
        headers = {}
        if require_auth and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        if use_json:
            headers["Content-Type"] = "application/json"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                if use_json:
                    response = self.session.post(
                        url, params=params, json=data, headers=headers
                    )
                else:
                    response = self.session.post(url, data=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() or {}

        except requests.exceptions.RequestException:
            # Log error and return empty dict
            return {}

    def start_device_auth(self) -> bool:
        """
        Start OAuth 2.0 Device Flow authentication

        Returns:
            bool: True if device code was obtained successfully
        """
        data = {
            "grant_type": "device_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self._make_request(
            "POST", "/oauth2/device", data=data, require_auth=False
        )

        if response and "code" in response:
            self.device_code = response["code"]
            self.user_code = response["user_code"]
            self.verification_uri = response["verification_uri"]
            self.expires_in = response.get("expires_in", 8600)
            self.interval = response.get("interval", 5)

            return True
        else:
            return False

    def wait_for_activation(self) -> bool:
        """
        Poll for device activation

        Returns:
            bool: True if successfully authenticated
        """
        if not self.device_code:
            return False

        start_time = time.time()

        while time.time() - start_time < (self.expires_in or 0):
            data = {
                "grant_type": "device_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": self.device_code,
            }

            try:
                url = f"{self.base_url}/oauth2/device"
                response = self.session.post(url, data=data)

                if response.status_code == 200:
                    # Success - we got the tokens
                    token_data = response.json()
                    self.access_token = token_data["access_token"]
                    self.refresh_token = token_data.get("refresh_token")

                    # Save tokens
                    self._save_tokens()

                    # Notify device
                    self.notify_device()

                    return True

                elif response.status_code == 400:
                    # Check if it's still pending
                    try:
                        error_data = response.json()
                        if error_data.get("error") == "authorization_pending":
                            time.sleep(self.interval)
                            continue
                        else:
                            return False
                    except Exception:
                        return False
                else:
                    return False

            except requests.exceptions.RequestException:
                return False

        return False

    def notify_device(self) -> None:
        """Notify kino.pub that device is connected"""
        if not self.access_token:
            return

        data = {
            "title": "Kodi Addon",
            "hardware": "Kodi",
            "software": "Kino.pub Addon/1.0",
        }

        params = {"access_token": self.access_token or ""}
        self._make_request(
            "POST", "/v1/device/notify", params=params, data=data, use_json=True
        )

    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using refresh token

        Returns:
            bool: True if token was refreshed successfully
        """
        if not self.refresh_token:
            return False

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        response = self._make_request(
            "POST", "/oauth2/token", data=data, require_auth=False
        )

        if response and "access_token" in response:
            self.access_token = response["access_token"]
            self.refresh_token = response.get("refresh_token")
            self._save_tokens()
            return True
        else:
            return False

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None

    def get_items(
        self, page: int = 1, perpage: int = 20, type_filter: str | None = None
    ) -> dict:
        """
        Get video content items

        Args:
            page: Page number
            perpage: Items per page
            type_filter: Content type filter (movie, serial, etc.)

        Returns:
            Dict: API response with items
        """
        params = {
            "access_token": self.access_token or "",
            "page": page,
            "perpage": perpage,
        }

        if type_filter:
            params["type"] = type_filter

        return self._make_request("GET", "/v1/items", params=params)

    def get_item_details(self, item_id: str) -> dict:
        """
        Get detailed information about specific item

        Args:
            item_id: Item ID

        Returns:
            Dict: Item details
        """
        params = {"access_token": self.access_token or ""}
        return self._make_request("GET", f"/v1/items/{item_id}", params=params)

    def search_content(self, query: str, page: int = 1, perpage: int = 20) -> dict:
        """
        Search for content

        Args:
            query: Search query
            page: Page number
            perpage: Items per page

        Returns:
            Dict: Search results
        """
        params = {
            "access_token": self.access_token,
            "q": query,
            "page": page,
            "perpage": perpage,
        }

        return self._make_request("GET", "/v1/items/search", params=params)

    def get_tv_channels(self) -> dict:
        """
        Get available TV channels

        Returns:
            Dict: TV channels list
        """
        params = {"access_token": self.access_token or ""}
        return self._make_request("GET", "/v1/tv/index", params=params)

    def get_genres(self, genre_type: str | None = None) -> dict:
        """
        Get available genres

        Args:
            genre_type: Genre type filter (movie, music, docu)

        Returns:
            Dict: Genres list
        """
        params = {"access_token": self.access_token or ""}
        if genre_type:
            params["type"] = genre_type

        return self._make_request("GET", "/v1/genres", params=params)
