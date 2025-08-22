#!/usr/bin/env python3
"""
Kino.pub Kodi Addon - Main Entry Point
=====================================

Main entry point for the Kino.pub Kodi addon using CodeQuick routing framework.
"""

import os
import sys

# Add lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from lib.router import KinoPubRouter

# Initialize the router
router = KinoPubRouter()

# Main entry point
if __name__ == '__main__':
    router.run()
