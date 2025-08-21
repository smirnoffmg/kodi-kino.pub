# 🎬 Modern Kodi Kino.pub Addon

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Kodi 19+](https://img.shields.io/badge/kodi-19%2B-green.svg)](https://kodi.tv/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Tests](https://github.com/smirnoffmg/kodi-kino.pub/workflows/Tests/badge.svg)](https://github.com/smirnoffmg/kodi-kino.pub/actions)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> Next-generation Kodi addon for [Kino.pub](https://kino.pub) streaming service. Built with Python 3.11+, featuring Netflix-style UI, lightning-fast performance, and cutting-edge development practices.

## ✨ Features

- 🎯 **Netflix-Style Interface** - Modern, intuitive UI with hero banners and content rows
- 🚀 **Lightning Fast Performance** - Advanced caching and background loading
- 📱 **Cross-Device Sync** - Resume playback across all your devices
- 🎨 **Adaptive Quality** - Automatic quality selection based on connection
- 🔍 **Smart Search** - Intelligent search with autocomplete and suggestions
- 📚 **Smart Watchlist** - Advanced watchlist management with categories
- 🎭 **Rich Content Details** - Comprehensive metadata with cast, crew, and ratings
- 🌍 **Multi-Language Support** - English, Russian, Ukrainian interface
- ♿ **Accessibility** - Full keyboard navigation and screen reader support

## 📦 Installation

### Option 1: Repository Installation (Recommended)
1. Download the [latest addon ZIP](https://github.com/smirnoffmg/kodi-kino.pub/releases/latest)
2. In Kodi: **Settings** → **Add-ons** → **Install from zip file**
3. Select the downloaded addon ZIP file

## 🚀 Quick Start

1. **Authentication**: Launch the addon and follow the on-screen device activation instructions
2. **Browse Content**: Navigate through movies, series, and collections using the intuitive interface
3. **Search**: Use the search function to find specific content
4. **Watchlist**: Add content to your watchlist for easy access
5. **Enjoy**: Start watching with automatic quality selection and progress sync

## 🎮 Usage

### Navigation
- **D-pad/Arrow keys**: Navigate through the interface
- **Enter/OK**: Select items and start playback
- **Back**: Return to previous screen
- **Context Menu**: Access additional options (Add to watchlist, etc.)

### Keyboard Shortcuts
- **S**: Open search
- **F**: Toggle favorites
- **Q**: Quality selection
- **I**: Show info dialog

## ⚙️ Configuration

Access addon settings through:
**Kodi Settings** → **Add-ons** → **My add-ons** → **Video add-ons** → **Kino.pub** → **Configure**

### Key Settings
- **Video Quality**: Preferred streaming quality (Auto/4K/1080p/720p/480p)
- **Subtitle Language**: Default subtitle language preference
- **Interface Theme**: Light/Dark theme selection
- **Parental Controls**: Content filtering options
- **Network**: Proxy and connection settings

## 🛠️ Development

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Kodi 19+ for testing

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/smirnoffmg/kodi-kino.pub.git
cd kodi-kino.pub

# Set up development environment (using uv)
uv python install 3.11
uv sync --all-extras

# Or using traditional pip
python -m pip install -e .[dev]

# Run quality checks
uv run ruff check .
uv run mypy lib/
uv run pytest
```

### Tech Stack
- **Python 3.11+** - Modern Python with latest features
- **uv** - Ultra-fast Python package management
- **pytest** - Testing framework with benchmarking
- **ruff** - Lightning-fast linting and formatting
- **mypy** - Static type checking

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=lib

# Run performance benchmarks
uv run pytest --benchmark-only

# Run specific test types
uv run pytest tests/unit/      # Unit tests only
uv run pytest tests/integration/  # Integration tests
```

### Building
```bash
# Build addon package
uv run python scripts/build_addon.py

# The package will be created as kodi-kino.pub.zip
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests
4. Run quality checks (`uv run ruff check . && uv run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/smirnoffmg/kodi-kino.pub/issues)
- **Discussions**: [GitHub Discussions](https://github.com/smirnoffmg/kodi-kino.pub/discussions)
- **Kodi Forum**: [Kodi Community Forum](https://forum.kodi.tv/)

## 🙏 Acknowledgments

- [Kino.pub](https://kino.pub) for the excellent streaming service
- [Kodi Team](https://kodi.tv) for the amazing media center platform
- [CodeQuick](https://github.com/peak3d/script.module.codequick) for the addon framework
- All contributors and users who make this project better

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/smirnoffmg/kodi-kino.pub?style=social)
![GitHub forks](https://img.shields.io/github/forks/smirnoffmg/kodi-kino.pub?style=social)
![GitHub issues](https://img.shields.io/github/issues/smirnoffmg/kodi-kino.pub)
![GitHub pull requests](https://img.shields.io/github/issues-pr/smirnoffmg/kodi-kino.pub)

---

**Made with ❤️ for the Kodi community**
