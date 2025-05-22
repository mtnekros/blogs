# Python Project Development Standards

## Overview

This document outlines the standardized practices for developing Python
projects within the team. Following these guidelines ensures code consistency,
improves collaboration, and enforces best practices across all projects.

## 1. Development Environment

### 1.1 Use a Common Code Editor

* **Visual Studio Code (VSCode)** is recommended for consistency across the team.

### 1.2 Recommended VSCode Extensions

Install the following extensions:

* **Pyright** (by Microsoft): Enables fast static type checking.
* **Ruff** (by [Astral](https://astral.sh)): Unified tool for linting and formatting.

### 1.3 Project Folder Structure

Adopt a consistent folder structure across all Python projects to improve readability and maintainability:

```
project/
│
├── src/                    # Application source code
│   └── your_module/        # Replace with your module/package name
│       ├── __init__.py
│       └── ...
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   └── test_*.py
├── pyproject.toml          # Central configuration for all tools
├── requirements.txt        # List of dependencies
└── README.md               # Project overview
```

### 1.4 Centralized Configuration

* Use **`pyproject.toml`** as the single source of configuration for all tools: `ruff`, `pyright`, `pytest`, etc.
* Avoid scattering tool configurations across multiple files like `.flake8`, `mypy.ini`, or `.pylintrc`.

---

## 2. Testing Guidelines

### 2.1 Unit Testing

* Use **pytest** for writing and executing unit tests.
* Structure tests in the `tests/` directory using the `test_*.py` convention.

### 2.2 Test Coverage

* Use **pytest-cov** to generate test coverage reports.
* Aim for high coverage but prioritize meaningful test cases over pure percentage metrics.

---

## 3. Static Type Checking with Pyright

### 3.1 Why Use Static Type Checking?

* Catches type-related bugs early without running the code.
* Improves readability and self-documentation of code via type hints.
* Enhances IDE support and auto-completion.

### 3.2 Adding Pyright to VSCode

* Install the **Pyright** extension from the VSCode marketplace.
* Add the following configuration in `pyproject.toml`:

```toml
[tool.pyright]
# Pyright docs: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#sample-pyprojecttoml-file

typeCheckingMode = "standard"   # Enforces recommended type-checking rules

include = ["src"]               # Folder to include in type checking

exclude = [                     # Common folders to exclude
    "**/node_modules",
    "**/__pycache__",
    "src/experimental",
    "src/typestubs"
]

ignore = ["src/oldstuff"]       # Completely ignore legacy or deprecated code

stubPath = "src/stubs"          # Custom .pyi stub files (optional)

reportMissingImports = "error"  # Enforce missing imports as errors
reportMissingTypeStubs = false # Don't error on missing type hints for 3rd-party libs

pythonVersion = "3.6"           # Minimum Python version supported
pythonPlatform = "Linux"        # Target platform

executionEnvironments = [
    { root = "src" }            # Define base environment for code analysis
]
```

---

## 4. Linting & Formatting with Ruff

### 4.1 Why Use Linting and Formatting?

* Enforces consistent style and structure across codebases.
* Detects common errors and security issues early.
* Reduces friction in code reviews and merge conflicts.
* Improves long-term maintainability and onboarding.

### 4.2 Installing Ruff

* Install the **Ruff** extension from astral.sh
* Ruff replaces tools like flake8, isort, pyupgrade, black, and more.

### 4.3 Sample `pyproject.toml` Configuration

```toml
[tool.ruff]
line-length = 120              # Maximum characters per line
target-version = "py310"       # Your project's Python version

[tool.ruff.lint]
# Enabled rules (grouped by plugin origin)
select = [
  "ANN",  # `flake8-annotations`: Checks for missing & incorrect type annotations (func args & rtypes)
  "B",    # `flake8-bugbear`: Checks for likely bugs or bad practises for python code
  "D",    # `pydocstyle`: Enforces docstring conventions
  "E",    # `pycodestyle`: Checks for style guide violations (Error Codes)
  "W",    # `pycodestyle`: Checks for style guide violations (Warning Codes)
  "F",    # `pyflakes`: Checks for undefined names, unused variables, etc.
  "I",    # `isort`: Checks for import order and formatting
  "S",    # `bandit`: Checks for security issues in Python code
  "SIM",  # `flake8-simplify`: Checks for code that can be simplified
  "TCH",  # `flake8-type-checking`: Checks for type checking import placement
  "UP",   # `pyupgrade`: Checks for code that can be upgraded to a newer version of Python
  "YTT"   # `flake8-y2020`: Checks for year 2020 compatibility issues
]

# Rules to ignore
ignore = [
  "ANN101",  # Ignore missing 'self' type annotation
  "S101"     # Allow usage of 'assert' (useful in tests)
]

[tool.ruff.format]
quote-style = "double"         # Enforce double quotes
indent-style = "space"         # Use spaces, not tabs
line-ending = "lf"             # Use LF for cross-platform compatibility
```

---

## Summary

| Task                 | Tool / File                   |
| -------------------- | ----------------------------- |
| Type Checking        | `pyright` in `pyproject.toml` |
| Linting & Formatting | `ruff` in `pyproject.toml`    |
| Unit Testing         | `pytest` in `tests/`          |
| Test Coverage        | `pytest-cov`                  |
| Central Config       | `pyproject.toml`              |
| Editor & Extensions  | VSCode + Pyright + Ruff       |
| Folder Structure     | Standardized (see above)      |


## For more config settings:
 * Learn more about ruff configuration at https://docs.astral.sh/ruff/rules/
 * Learn more about pyright configuration at https://github.com/microsoft/pyright/blob/main/docs/configuration.md#sample-pyprojecttoml-file


