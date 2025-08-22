#!/usr/bin/env python3
"""
Kino.pub API Test Script - Device Authentication
===============================================

This script demonstrates how to interact with the kino.pub API using Python
with OAuth 2.0 Device Flow authentication. No personal client_id needed!

Requirements:
- requests library: pip install requests

Usage:
1. Run the script
2. Follow the device activation prompts (visit kino.pub/device)
3. Enter the code shown on screen
4. Explore the API functionality
"""

import json
import sys
import time
from urllib.parse import urljoin

import requests


class KinoPubAPI:
    """
    Kino.pub API Client with Device Flow Authentication

    Uses public device credentials for OAuth 2.0 Device Flow authentication.
    """

    def __init__(self):
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
                "User-Agent": "KinoPub-Python-Test/1.0",
            }
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
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
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error response: {json.dumps(error_data, indent=2)}")
                except Exception:
                    print(f"Error response text: {e.response.text}")
            return {}

    def start_device_auth(self) -> bool:
        """
        Start OAuth 2.0 Device Flow authentication

        Returns:
            bool: True if device code was obtained successfully
        """
        print("🔐 Starting device authentication...")

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

            print("✅ Device code obtained!")
            print(f"📱 Please visit: {self.verification_uri}")
            print(f"🔑 Enter this code: {self.user_code}")
            print(f"⏱️  Code expires in {self.expires_in} seconds")
            print(f"⏰ Will check every {self.interval} seconds for activation...")

            return True
        else:
            print("❌ Failed to get device code")
            return False

    def wait_for_activation(self) -> bool:
        """
        Poll for device activation

        Returns:
            bool: True if successfully authenticated
        """
        if not self.device_code:
            print("❌ No device code available. Call start_device_auth() first.")
            return False

        print("\n⏳ Waiting for device activation...")
        print(
            "💡 Please enter the code on the website and then press Enter here to continue checking..."
        )
        input("🔄 Press Enter after entering the code on kino.pub/device...")

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < self.expires_in:
            attempt += 1
            data = {
                "grant_type": "device_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": self.device_code,
            }

            print(f"🔍 Checking activation status (attempt {attempt})...")

            # Make request without using the error-handling wrapper for auth polling
            try:
                url = f"{self.base_url}/oauth2/device"
                response = self.session.post(url, data=data)

                if response.status_code == 200:
                    # Success - we got the tokens
                    token_data = response.json()
                    self.access_token = token_data["access_token"]
                    self.refresh_token = token_data.get("refresh_token")

                    print("✅ Authentication successful!")
                    print(
                        f"🎯 Access token obtained (expires in {token_data.get('expires_in', 'unknown')} seconds)"
                    )

                    # Notify device
                    self.notify_device()

                    return True

                elif response.status_code == 400:
                    # Check if it's still pending
                    try:
                        error_data = response.json()
                        if error_data.get("error") == "authorization_pending":
                            print("⏳ Still waiting for activation... (this is normal)")
                            print(
                                f"⏰ Time remaining: {int(self.expires_in - (time.time() - start_time))} seconds"
                            )
                            time.sleep(self.interval)
                            continue
                        else:
                            print(f"❌ Authentication error: {error_data}")
                            return False
                    except Exception:
                        print(f"❌ Unexpected error response: {response.text}")
                        return False

                else:
                    print(f"❌ HTTP error {response.status_code}: {response.text}")
                    return False

            except requests.exceptions.RequestException as e:
                print(f"❌ Network error: {e}")
                return False

        print("⏰ Device code expired")
        return False

    def notify_device(self):
        """Notify kino.pub that device is connected"""
        if not self.access_token:
            return

        data = {
            "title": "Python Test Client",
            "hardware": "PC",
            "software": "Python/Test",
        }

        params = {"access_token": self.access_token}
        response = self._make_request(
            "POST", "/v1/device/notify", params=params, data=data, use_json=True
        )

        if response:
            print("📱 Device notification sent")

    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using refresh token

        Returns:
            bool: True if token was refreshed successfully
        """
        if not self.refresh_token:
            print("❌ No refresh token available")
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
            print("✅ Token refreshed successfully!")
            return True
        else:
            print("❌ Failed to refresh token")
            return False

    def get_items(
        self, page: int = 1, perpage: int = 10, type_filter: str = None
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
        params = {"access_token": self.access_token, "page": page, "perpage": perpage}

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
        params = {"access_token": self.access_token}
        return self._make_request("GET", f"/v1/items/{item_id}", params=params)

    def search_content(self, query: str, page: int = 1, perpage: int = 10) -> dict:
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
        params = {"access_token": self.access_token}
        return self._make_request("GET", "/v1/tv/index", params=params)

    def get_genres(self, genre_type: str = None) -> dict:
        """
        Get available genres

        Args:
            genre_type: Genre type filter (movie, music, docu)

        Returns:
            Dict: Genres list
        """
        params = {"access_token": self.access_token}
        if genre_type:
            params["type"] = genre_type

        return self._make_request("GET", "/v1/genres", params=params)


def print_items(items_data: dict):
    """Helper function to print items in a nice format"""
    if not items_data or "items" not in items_data:
        print("❌ No items found")
        return

    items = items_data["items"]
    pagination = items_data.get("pagination", {})

    print(
        f"\n📺 Found {len(items)} items (Total: {pagination.get('total', 'unknown')})"
    )
    print("=" * 80)

    for item in items[:5]:  # Show first 5 items
        print(f"🎬 {item.get('title', 'Unknown Title')}")
        print(f"   📅 Year: {item.get('year', 'Unknown')}")
        print(f"   🎭 Type: {item.get('type', 'Unknown')}")
        print(f"   ⭐ Quality: {item.get('quality', 'Unknown')}p")
        if item.get("plot"):
            plot = (
                item["plot"][:100] + "..." if len(item["plot"]) > 100 else item["plot"]
            )
            print(f"   📝 Plot: {plot}")
        print()


def main():
    """Main test function"""
    print("🎬 Kino.pub API Test Script")
    print("=" * 40)

    # Initialize API client
    api = KinoPubAPI()

    # Step 1: Start device authentication
    if not api.start_device_auth():
        print("❌ Failed to start authentication")
        return

    # Step 2: Wait for user to activate device
    if not api.wait_for_activation():
        print("❌ Authentication failed")
        return

    print("\n🎉 Authentication successful! Testing API endpoints...")
    print("=" * 60)

    # Test 1: Get recent movies
    print("\n1️⃣ Testing: Get recent movies")
    movies = api.get_items(page=1, perpage=5, type_filter="movie")
    print_items(movies)

    # Test 2: Get recent TV series
    print("\n2️⃣ Testing: Get recent TV series")
    series = api.get_items(page=1, perpage=5, type_filter="serial")
    print_items(series)

    # Test 3: Search functionality
    print("\n3️⃣ Testing: Search functionality")
    search_query = input("Enter search term (or press Enter for 'Marvel'): ").strip()
    if not search_query:
        search_query = "Marvel"

    search_results = api.search_content(search_query, perpage=3)
    print(f"🔍 Search results for '{search_query}':")
    print_items(search_results)

    # Test 4: Get genres
    print("\n4️⃣ Testing: Get movie genres")
    genres = api.get_genres("movie")
    if genres and "genres" in genres:
        print("🎭 Available movie genres:")
        for genre in genres["genres"][:10]:  # Show first 10
            print(f"   • {genre.get('title', 'Unknown')}")

    # Test 5: TV Channels
    print("\n5️⃣ Testing: Get TV channels")
    tv_channels = api.get_tv_channels()
    if tv_channels and "channels" in tv_channels:
        print(f"📺 Found {len(tv_channels['channels'])} TV channels:")
        for channel in tv_channels["channels"][:5]:  # Show first 5
            print(f"   📡 {channel.get('title', 'Unknown Channel')}")

    # Test 6: Item details (if we have any items)
    if movies and movies.get("items"):
        print("\n6️⃣ Testing: Get item details")
        first_movie = movies["items"][0]
        movie_id = first_movie.get("id")
        if movie_id:
            details = api.get_item_details(movie_id)
            if details and "item" in details:
                item = details["item"]
                print(f"🎬 Details for: {item.get('title', 'Unknown')}")
                print(f"   🎭 Cast: {item.get('cast', 'Unknown')}")
                print(f"   🎬 Director: {item.get('director', 'Unknown')}")
                print(
                    f"   🌍 Countries: {', '.join([c.get('title', '') for c in item.get('countries', [])])}"
                )

                # Show available videos/seasons
                if item.get("videos"):
                    print(f"   📹 Videos available: {len(item['videos'])}")
                elif item.get("seasons"):
                    print(f"   📺 Seasons available: {len(item['seasons'])}")

    print("\n✅ API testing completed!")
    print("\n💡 Tips:")
    print("   • Your access token is valid for 1 hour")
    print("   • Use refresh token to get new access token")
    print("   • Check API documentation at https://kinoapi.com")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
