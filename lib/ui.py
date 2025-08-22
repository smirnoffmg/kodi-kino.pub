#!/usr/bin/env python3
"""
Kino.pub UI Components
=====================

UI components and helpers for the Kino.pub Kodi addon.
"""

from typing import Any

import xbmcaddon
import xbmcgui


class KinoPubUI:
    """UI components for Kino.pub addon"""

    def __init__(self):
        self.addon = xbmcaddon.Addon()

    def create_content_item(self, item: dict[str, Any]) -> xbmcgui.ListItem:
        """
        Create a Kodi ListItem from content data

        Args:
            item: Content item data from API

        Returns:
            xbmcgui.ListItem: Configured list item
        """
        # Extract basic info
        title = item.get("title", "")
        year = item.get("year", "")
        plot = item.get("plot", "")
        type_ = item.get("type", "")

        # Create list item
        list_item = xbmcgui.ListItem(
            label=title,
            iconImage=self._get_item_icon(item),
            thumbnailImage=self._get_item_thumbnail(item),
        )

        # Set art
        list_item.setArt(
            {
                "fanart": self._get_item_fanart(item),
                "icon": self._get_item_icon(item),
                "thumb": self._get_item_thumbnail(item),
                "poster": self._get_item_poster(item),
            }
        )

        # Set video info
        video_info = {
            "title": title,
            "year": year,
            "plot": plot,
            "genre": self._get_genres(item),
            "director": self._get_director(item),
            "cast": self._get_cast(item),
            "duration": self._get_duration(item),
            "rating": self._get_rating(item),
            "mpaa": self._get_mpaa(item),
            "mediatype": self._get_mediatype(type_),
        }

        list_item.setInfo("video", video_info)

        # Add context menu
        context_menu = self._create_context_menu(item)
        list_item.addContextMenuItems(context_menu)

        # Set properties
        list_item.setProperty("IsPlayable", "true")
        list_item.setProperty("IsFolder", "false")

        return list_item

    def _get_item_icon(self, item: dict[str, Any]) -> str:
        """Get item icon path"""
        # Default icon based on content type
        type_ = item.get("type", "")
        if type_ == "movie":
            return "movie.png"
        elif type_ == "serial":
            return "tv.png"
        else:
            return "video.png"

    def _get_item_thumbnail(self, item: dict[str, Any]) -> str:
        """Get item thumbnail path"""
        # Use poster if available, otherwise default
        poster = item.get("poster", {})
        if poster and "url" in poster:
            return poster["url"]
        return self._get_item_icon(item)

    def _get_item_poster(self, item: dict[str, Any]) -> str:
        """Get item poster path"""
        poster = item.get("poster", {})
        if poster and "url" in poster:
            return poster["url"]
        return self._get_item_icon(item)

    def _get_item_fanart(self, item: dict[str, Any]) -> str:
        """Get item fanart path"""
        fanart = item.get("fanart", {})
        if fanart and "url" in fanart:
            return fanart["url"]
        return "fanart.jpg"

    def _get_genres(self, item: dict[str, Any]) -> str:
        """Get genres as string"""
        genres = item.get("genres", [])
        if genres:
            return ", ".join([g.get("title", "") for g in genres])
        return ""

    def _get_director(self, item: dict[str, Any]) -> str:
        """Get director as string"""
        director = item.get("director", "")
        if director:
            return director
        return ""

    def _get_cast(self, item: dict[str, Any]) -> str:
        """Get cast as string"""
        cast = item.get("cast", "")
        if cast:
            return cast
        return ""

    def _get_duration(self, item: dict[str, Any]) -> int:
        """Get duration in minutes"""
        duration = item.get("duration", 0)
        if duration:
            return int(duration)
        return 0

    def _get_rating(self, item: dict[str, Any]) -> float:
        """Get rating"""
        rating = item.get("rating", {})
        if rating and "kp" in rating:
            return float(rating["kp"])
        return 0.0

    def _get_mpaa(self, item: dict[str, Any]) -> str:
        """Get MPAA rating"""
        mpaa = item.get("mpaa", "")
        if mpaa:
            return mpaa
        return ""

    def _get_mediatype(self, type_: str) -> str:
        """Get Kodi media type"""
        if type_ == "movie":
            return "movie"
        elif type_ == "serial":
            return "tvshow"
        else:
            return "video"

    def _create_context_menu(self, item: dict[str, Any]) -> list:
        """Create context menu for item"""
        context_menu = []

        # Add to watchlist
        context_menu.append(
            (
                self.addon.getLocalizedString(30042),  # "Add to Watchlist"
                f"RunPlugin(/watchlist/add/{item.get('id')})",
            )
        )

        # Show details
        context_menu.append(
            (
                self.addon.getLocalizedString(30043),  # "Show Details"
                f"RunPlugin(/details/{item.get('id')})",
            )
        )

        # Play with quality selection
        context_menu.append(
            (
                self.addon.getLocalizedString(30044),  # "Play with Quality Selection"
                f"RunPlugin(/play/quality/{item.get('id')})",
            )
        )

        return context_menu

    def show_error_dialog(self, title: str, message: str):
        """Show error dialog"""
        dialog = xbmcgui.Dialog()
        dialog.ok(title, message)

    def show_info_dialog(self, title: str, message: str):
        """Show info dialog"""
        dialog = xbmcgui.Dialog()
        dialog.ok(title, message)

    def show_yes_no_dialog(self, title: str, message: str) -> bool:
        """Show yes/no dialog"""
        dialog = xbmcgui.Dialog()
        return dialog.yesno(title, message)

    def show_input_dialog(self, title: str, message: str) -> str:
        """Show input dialog"""
        dialog = xbmcgui.Dialog()
        return dialog.input(title, message)

    def show_progress_dialog(self, title: str, message: str):
        """Show progress dialog"""
        dialog = xbmcgui.DialogProgress()
        dialog.create(title, message)
        return dialog

    def create_quality_menu(self, item_id: str, qualities: list) -> list:
        """Create quality selection menu"""
        menu_items = []

        for quality in qualities:
            label = f"{quality.get('quality', 'Unknown')}p"
            if quality.get("size"):
                label += f" ({quality['size']})"

            menu_items.append(
                (label, f"RunPlugin(/play/quality/{item_id}/{quality.get('id')})")
            )

        return menu_items
