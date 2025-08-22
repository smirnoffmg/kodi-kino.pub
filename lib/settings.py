#!/usr/bin/env python3
"""
Kino.pub Settings
================

Settings management for the Kino.pub Kodi addon.
"""


import xbmcaddon


class KinoPubSettings:
    """Settings management for Kino.pub addon"""

    def __init__(self):
        self.addon = xbmcaddon.Addon()

    def get_video_quality(self) -> str:
        """Get preferred video quality setting"""
        return self.addon.getSetting('video_quality') or 'auto'

    def set_video_quality(self, quality: str):
        """Set preferred video quality setting"""
        self.addon.setSetting('video_quality', quality)

    def get_subtitle_language(self) -> str:
        """Get preferred subtitle language setting"""
        return self.addon.getSetting('subtitle_language') or 'ru'

    def set_subtitle_language(self, language: str):
        """Set preferred subtitle language setting"""
        self.addon.setSetting('subtitle_language', language)

    def get_interface_theme(self) -> str:
        """Get interface theme setting"""
        return self.addon.getSetting('interface_theme') or 'dark'

    def set_interface_theme(self, theme: str):
        """Set interface theme setting"""
        self.addon.setSetting('interface_theme', theme)

    def get_parental_controls(self) -> bool:
        """Get parental controls setting"""
        return self.addon.getSetting('parental_controls') == 'true'

    def set_parental_controls(self, enabled: bool):
        """Set parental controls setting"""
        self.addon.setSetting('parental_controls', 'true' if enabled else 'false')

    def get_auto_login(self) -> bool:
        """Get auto login setting"""
        return self.addon.getSetting('auto_login') == 'true'

    def set_auto_login(self, enabled: bool):
        """Set auto login setting"""
        self.addon.setSetting('auto_login', 'true' if enabled else 'false')

    def get_cache_enabled(self) -> bool:
        """Get cache enabled setting"""
        return self.addon.getSetting('cache_enabled') == 'true'

    def set_cache_enabled(self, enabled: bool):
        """Set cache enabled setting"""
        self.addon.setSetting('cache_enabled', 'true' if enabled else 'false')

    def get_cache_duration(self) -> int:
        """Get cache duration setting in seconds"""
        try:
            return int(self.addon.getSetting('cache_duration') or '3600')
        except ValueError:
            return 3600

    def set_cache_duration(self, duration: int):
        """Set cache duration setting in seconds"""
        self.addon.setSetting('cache_duration', str(duration))

    def get_setting(self, setting_id: str) -> str:
        """Get any setting by ID"""
        return self.addon.getSetting(setting_id) or ''

    def set_setting(self, setting_id: str, value: str):
        """Set any setting by ID"""
        self.addon.setSetting(setting_id, value)

    def get_boolean_setting(self, setting_id: str) -> bool:
        """Get boolean setting by ID"""
        return self.addon.getSetting(setting_id) == 'true'

    def set_boolean_setting(self, setting_id: str, value: bool):
        """Set boolean setting by ID"""
        self.addon.setSetting(setting_id, 'true' if value else 'false')

    def get_int_setting(self, setting_id: str, default: int = 0) -> int:
        """Get integer setting by ID"""
        try:
            return int(self.addon.getSetting(setting_id) or str(default))
        except ValueError:
            return default

    def set_int_setting(self, setting_id: str, value: int):
        """Set integer setting by ID"""
        self.addon.setSetting(setting_id, str(value))

    def get_float_setting(self, setting_id: str, default: float = 0.0) -> float:
        """Get float setting by ID"""
        try:
            return float(self.addon.getSetting(setting_id) or str(default))
        except ValueError:
            return default

    def set_float_setting(self, setting_id: str, value: float):
        """Set float setting by ID"""
        self.addon.setSetting(setting_id, str(value))

    def open_settings(self):
        """Open addon settings dialog"""
        self.addon.openSettings()

    def get_addon_info(self, info_id: str) -> str:
        """Get addon information"""
        return self.addon.getAddonInfo(info_id)

    def get_localized_string(self, string_id: int) -> str:
        """Get localized string"""
        return self.addon.getLocalizedString(string_id)

    def get_quality_options(self) -> list:
        """Get available quality options"""
        return [
            {'id': 'auto', 'label': self.get_localized_string(30002)},
            {'id': '4k', 'label': self.get_localized_string(30003)},
            {'id': '1080p', 'label': self.get_localized_string(30004)},
            {'id': '720p', 'label': self.get_localized_string(30005)},
            {'id': '480p', 'label': self.get_localized_string(30006)}
        ]

    def get_language_options(self) -> list:
        """Get available language options"""
        return [
            {'id': 'ru', 'label': self.get_localized_string(30008)},
            {'id': 'en', 'label': self.get_localized_string(30009)},
            {'id': 'uk', 'label': self.get_localized_string(30010)}
        ]

    def get_theme_options(self) -> list:
        """Get available theme options"""
        return [
            {'id': 'dark', 'label': self.get_localized_string(30012)},
            {'id': 'light', 'label': self.get_localized_string(30013)}
        ]

    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.set_video_quality('auto')
        self.set_subtitle_language('ru')
        self.set_interface_theme('dark')
        self.set_parental_controls(False)
        self.set_auto_login(True)
        self.set_cache_enabled(True)
        self.set_cache_duration(3600)
