#!/usr/bin/env python3
"""
Kino.pub Router
==============

Main router for the Kino.pub Kodi addon using CodeQuick framework.
"""


import codequick
import xbmcaddon
import xbmcgui

from .api import KinoPubAPI
from .settings import KinoPubSettings
from .ui import KinoPubUI


class KinoPubRouter:
    """Main router for Kino.pub addon"""

    def __init__(self):
        self.api = KinoPubAPI()
        self.ui = KinoPubUI()
        self.settings = KinoPubSettings()
        self.addon = xbmcaddon.Addon()

    def run(self):
        """Start the router"""
        # Check authentication first
        if not self.api.is_authenticated():
            self._handle_authentication()

        # Show main menu
        self._show_main_menu()

    def _handle_authentication(self):
        """Handle OAuth 2.0 Device Flow authentication"""
        dialog = xbmcgui.Dialog()

        # Start device authentication
        if not self.api.start_device_auth():
            dialog.ok(
                self.addon.getLocalizedString(30018),  # "Authentication Error"
                self.addon.getLocalizedString(30019)   # "Failed to start authentication"
            )
            return False

        # Show device activation dialog
        dialog.ok(
            self.addon.getLocalizedString(30020),  # "Device Activation Required"
            f"{self.addon.getLocalizedString(30021)}: {self.api.verification_uri}\n\n"  # "Please visit"
            f"{self.addon.getLocalizedString(30022)}: {self.api.user_code}",  # "Enter this code"
        )

        # Wait for activation
        progress = xbmcgui.DialogProgress()
        progress.create(
            self.addon.getLocalizedString(30023),  # "Waiting for Activation"
            self.addon.getLocalizedString(30024)   # "Please complete activation on the website"
        )

        if self.api.wait_for_activation():
            progress.close()
            dialog.ok(
                self.addon.getLocalizedString(30025),  # "Success"
                self.addon.getLocalizedString(30026)   # "Authentication successful"
            )
            return True
        else:
            progress.close()
            dialog.ok(
                self.addon.getLocalizedString(30027),  # "Authentication Failed"
                self.addon.getLocalizedString(30028)   # "Please try again"
            )
            return False

    def _show_main_menu(self):
        """Show the main menu"""
        items = [
            {
                'label': self.addon.getLocalizedString(30029),  # "Movies"
                'url': '/movies',
                'icon': 'movies.png',
                'fanart': 'fanart.jpg'
            },
            {
                'label': self.addon.getLocalizedString(30030),  # "TV Shows"
                'url': '/tv',
                'icon': 'tv.png',
                'fanart': 'fanart.jpg'
            },
            {
                'label': self.addon.getLocalizedString(30031),  # "Search"
                'url': '/search',
                'icon': 'search.png',
                'fanart': 'fanart.jpg'
            },
            {
                'label': self.addon.getLocalizedString(30032),  # "TV Channels"
                'url': '/channels',
                'icon': 'channels.png',
                'fanart': 'fanart.jpg'
            },
            {
                'label': self.addon.getLocalizedString(30033),  # "Genres"
                'url': '/genres',
                'icon': 'genres.png',
                'fanart': 'fanart.jpg'
            },
            {
                'label': self.addon.getLocalizedString(30034),  # "Settings"
                'url': '/settings',
                'icon': 'settings.png',
                'fanart': 'fanart.jpg'
            }
        ]

        # Add items to Kodi
        for item in items:
            list_item = xbmcgui.ListItem(
                label=item['label'],
                iconImage=item['icon'],
                thumbnailImage=item['icon']
            )
            list_item.setArt({
                'fanart': item['fanart'],
                'icon': item['icon'],
                'thumb': item['icon']
            })

            # Add context menu
            context_menu = [
                (self.addon.getLocalizedString(30035), f"RunPlugin({item['url']})")  # "Open"
            ]
            list_item.addContextMenuItems(context_menu)

            # Add to directory
            codequick.listitem.add(list_item, item['url'])

        # Set content type
        codequick.listitem.set_content_type('videos')

    @codequick.route('/movies')
    def movies(self):
        """Show movies listing"""
        return self._show_content_list('movie')

    @codequick.route('/tv')
    def tv_shows(self):
        """Show TV shows listing"""
        return self._show_content_list('serial')

    @codequick.route('/search')
    def search(self):
        """Show search interface"""
        dialog = xbmcgui.Dialog()
        query = dialog.input(self.addon.getLocalizedString(30036))  # "Enter search term"

        if query:
            return self._show_search_results(query)
        else:
            return self._show_main_menu()

    @codequick.route('/channels')
    def channels(self):
        """Show TV channels"""
        channels_data = self.api.get_tv_channels()

        if not channels_data or 'channels' not in channels_data:
            xbmcgui.Dialog().ok(
                self.addon.getLocalizedString(30037),  # "Error"
                self.addon.getLocalizedString(30038)   # "Failed to load channels"
            )
            return

        for channel in channels_data['channels']:
            list_item = xbmcgui.ListItem(
                label=channel.get('title', 'Unknown Channel'),
                iconImage='channel.png',
                thumbnailImage='channel.png'
            )

            # Add stream info
            list_item.setInfo('video', {
                'title': channel.get('title'),
                'plot': channel.get('description', ''),
            })

            # Add to directory
            codequick.listitem.add(list_item, f"/play/channel/{channel.get('id')}")

        codequick.listitem.set_content_type('videos')

    @codequick.route('/genres')
    def genres(self):
        """Show genres"""
        genres_data = self.api.get_genres('movie')

        if not genres_data or 'genres' not in genres_data:
            xbmcgui.Dialog().ok(
                self.addon.getLocalizedString(30037),  # "Error"
                self.addon.getLocalizedString(30039)   # "Failed to load genres"
            )
            return

        for genre in genres_data['genres']:
            list_item = xbmcgui.ListItem(
                label=genre.get('title', 'Unknown Genre'),
                iconImage='genre.png',
                thumbnailImage='genre.png'
            )

            # Add to directory
            codequick.listitem.add(list_item, f"/genre/{genre.get('id')}")

        codequick.listitem.set_content_type('videos')

    @codequick.route('/settings')
    def settings(self):
        """Open addon settings"""
        self.addon.openSettings()
        return self._show_main_menu()

    def _show_content_list(self, content_type: str):
        """Show content listing for movies or TV shows"""
        content_data = self.api.get_items(page=1, perpage=20, type_filter=content_type)

        if not content_data or 'items' not in content_data:
            xbmcgui.Dialog().ok(
                self.addon.getLocalizedString(30037),  # "Error"
                self.addon.getLocalizedString(30040)   # "Failed to load content"
            )
            return

        for item in content_data['items']:
            list_item = self.ui.create_content_item(item)
            codequick.listitem.add(list_item, f"/play/{item.get('id')}")

        codequick.listitem.set_content_type('videos')

    def _show_search_results(self, query: str):
        """Show search results"""
        search_data = self.api.search_content(query, page=1, perpage=20)

        if not search_data or 'items' not in search_data:
            xbmcgui.Dialog().ok(
                self.addon.getLocalizedString(30037),  # "Error"
                self.addon.getLocalizedString(30041)   # "No results found"
            )
            return

        for item in search_data['items']:
            list_item = self.ui.create_content_item(item)
            codequick.listitem.add(list_item, f"/play/{item.get('id')}")

        codequick.listitem.set_content_type('videos')
