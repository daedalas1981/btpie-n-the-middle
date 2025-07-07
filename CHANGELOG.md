# 📦 CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2025-07-04

### 🚀 Added
- Initial fully modular MITM relay core (`core.py`, `adapter.py`, `logger.py`, `utils.py`)
- Two-way RFCOMM proxy between master and slave Bluetooth devices
- Timestamped hex logging to `logs/` directory
- CLI entry via `scripts/btpie.py` with flags: `--mitm`, `--master`, `--slave`, `--log`, `--port`, `--verbose`, `--trust`, `--untrust`, `--scan`, `--paired`
- Interactive script (`interactive_btpie.py`) with guided setup prompts
- Full test suite with `pytest` and six dedicated test modules
- Project structure documentation in `README.md` and `tests/README.md`
- MIT license and GitHub workflow files
- `.gitignore` and `setup.py` configuration for manual use and packaging

### 🛠 Changed
- Improved `logger.py` to ensure log directory creation
- Updated `setup.py` with metadata, entry points, and optional dependency handling
- Enhanced pairing and Bluetooth scanning logic with error fallback messages

---

## [Unreleased]

- BLE support
- Traffic summarization and analytics
- Interactive mode auto-retry logic
- `.deb` installer support
