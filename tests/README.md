# 🧪 BTPIE Test Suite

This folder contains automated unit tests for the BTPIE-N-THE-MIDDLE project.

Tests are written using [pytest](https://docs.pytest.org/) and cover core functionality, logging, utilities, and CLI behavior.

## 🗂 Structure

```text
tests/
├── test_adapter.py       # Bluetooth adapter logic
├── test_core.py          # MITM core initialization and cleanup
├── test_logger.py        # Logger creation and output
├── test_utils.py         # Utility helpers (e.g., hex formatting, timestamps)
├── test_interactive.py   # Bluetoothctl handling and pairing checks
├── test_btpie.py         # CLI flag parsing and validation
```

## ▶️ Running Tests

From the project root:

```bash
pytest tests/
```

## 🧪 Coverage Reporting (Optional)

To see how much of the codebase is exercised by the tests:

```bash
pip install pytest-cov
pytest --cov=btpie tests/
```

Generate a detailed HTML report:

```bash
pytest --cov=btpie --cov-report=html tests/
xdg-open htmlcov/index.html
```

## ✅ Notes

- Uses `unittest.mock` to isolate dependencies
- Verifies CLI flags, logger output, utility behavior, and pairing logic
- Tests run independently and use `tmp_path` where needed for file isolation

---
Built by Robert Cole as part of the BTPIE project.
