# 🧪 BTPIE Test Suite

This folder contains automated unit tests for the BTPIE-N-THE-MIDDLE project.

Tests are written using [pytest](https://docs.pytest.org/) and cover core functionality, logging, utilities, and interactive logic.

## 🗂 Structure

```text
tests/
├── test_adapter.py       # Bluetooth adapter logic
├── test_core.py          # MITM core initialization and cleanup
├── test_logger.py        # Logger creation and output
├── test_utils.py         # Utility helpers (e.g., hex formatting, timestamps)
├── test_interactive.py   # Bluetoothctl handling and pairing checks
```

## ▶️ Running Tests

From the project root:

```bash
pytest tests/
```

## ✅ Notes

- Tests use `tmp_path` for isolated log file validation
- System-level Bluetooth behavior is mocked where needed
- Additional tests planned for `btpie.py` argument parsing and CLI logic

---
Built by Robert Cole as part of the BTPIE project.
