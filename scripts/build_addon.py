#!/usr/bin/env python3
"""
Build Script for Kino.pub Kodi Addon
===================================

Script to build and package the Kino.pub Kodi addon for distribution.
"""

import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path


def get_addon_version():
    """Get addon version from addon.xml"""
    addon_xml_path = Path("addon.xml")
    if not addon_xml_path.exists():
        return "1.0.0"

    with open(addon_xml_path, encoding="utf-8") as f:
        content = f.read()
        # Simple version extraction
        if 'version="' in content:
            start = content.find('version="') + 9
            end = content.find('"', start)
            return content[start:end]

    return "1.0.0"


def create_addon_package():
    """Create the addon package ZIP file"""
    version = get_addon_version()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"plugin.video.kinopub-{version}-{timestamp}.zip"

    # Files and directories to include
    include_paths = [
        "addon.xml",
        "default.py",
        "lib/",
        "resources/",
        "LICENSE",
        "README.md",
    ]

    # Files to exclude
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        "Thumbs.db",
        ".git",
        ".gitignore",
        "tests/",
        "scripts/",
        "api-test.py",
        "pyproject.toml",
        "requirements.txt",
    ]

    print(f"Building addon package: {package_name}")
    print(f"Version: {version}")
    print(f"Timestamp: {timestamp}")

    with zipfile.ZipFile(package_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for include_path in include_paths:
            if os.path.exists(include_path):
                if os.path.isdir(include_path):
                    # Add directory contents
                    for root, dirs, files in os.walk(include_path):
                        # Filter out excluded directories
                        dirs[:] = [d for d in dirs if d not in exclude_patterns]

                        for file in files:
                            file_path = os.path.join(root, file)

                            # Check if file should be excluded
                            should_exclude = False
                            for pattern in exclude_patterns:
                                if pattern in file_path or file_path.endswith(pattern):
                                    should_exclude = True
                                    break

                            if not should_exclude:
                                arcname = os.path.relpath(file_path)
                                print(f"Adding: {arcname}")
                                zipf.write(file_path, arcname)
                else:
                    # Add single file
                    print(f"Adding: {include_path}")
                    zipf.write(include_path, include_path)
            else:
                print(f"Warning: {include_path} not found")

    print(f"\nPackage created successfully: {package_name}")
    print(f"Package size: {os.path.getsize(package_name) / 1024:.1f} KB")

    return package_name


def create_repository_package():
    """Create repository package for addon distribution"""
    version = get_addon_version()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_name = f"kinopub-repository-{version}-{timestamp}.zip"

    # Create repository structure
    repo_dir = Path("repository")
    repo_dir.mkdir(exist_ok=True)

    # Copy addon to repository
    addon_dir = repo_dir / "plugin.video.kinopub"
    addon_dir.mkdir(exist_ok=True)

    # Copy addon files
    addon_files = [
        "addon.xml",
        "default.py",
        "lib/",
        "resources/",
    ]

    for file_path in addon_files:
        src = Path(file_path)
        dst = addon_dir / file_path

        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

    # Create repository.xml
    repo_xml_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addons>
    <addon id="plugin.video.kinopub" name="Kino.pub" version="{version}" provider-name="smirnoffmg">
        <requires>
            <import addon="xbmc.python" version="3.0.0"/>
            <import addon="script.module.codequick" version="0.0.1"/>
            <import addon="script.module.requests" version="2.25.1"/>
        </requires>
        <extension point="xbmc.python.pluginsource" library="default.py">
            <provides>video</provides>
        </extension>
        <extension point="xbmc.addon.metadata">
            <summary lang="en">Modern Kodi addon for Kino.pub streaming service</summary>
            <description lang="en">Next-generation Kodi addon for Kino.pub streaming service.</description>
            <platform>all</platform>
            <language>en</language>
            <language>ru</language>
            <language>uk</language>
            <license>GPL-3.0</license>
            <forum>https://github.com/smirnoffmg/kodi-kino.pub/discussions</forum>
            <website>https://github.com/smirnoffmg/kodi-kino.pub</website>
            <source>https://github.com/smirnoffmg/kodi-kino.pub</source>
        </extension>
    </addon>
</addons>"""

    with open(repo_dir / "repository.xml", "w", encoding="utf-8") as f:
        f.write(repo_xml_content)

    # Create ZIP package
    with zipfile.ZipFile(repo_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _dirs, files in os.walk(repo_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, repo_dir.parent)
                zipf.write(file_path, arcname)

    # Clean up
    shutil.rmtree(repo_dir)

    print(f"Repository package created: {repo_name}")
    return repo_name


def main():
    """Main build function"""
    print("Kino.pub Kodi Addon Build Script")
    print("=" * 40)

    # Check if we're in the right directory
    if not os.path.exists("addon.xml"):
        print(
            "Error: addon.xml not found. Please run this script from the addon root directory."
        )
        sys.exit(1)

    try:
        # Create addon package
        addon_package = create_addon_package()

        # Create repository package
        repo_package = create_repository_package()

        print("\nBuild completed successfully!")
        print(f"Addon package: {addon_package}")
        print(f"Repository package: {repo_package}")

    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
