# Development Environment Setup Instruction
## Text Editor 
* VSCode


## VSCode Extensions to install:
    1. Python (By Microsoft) (For General intellisense & testing too)
    2. Ruff (By Astral) (For linting & formatting)
    3. Pyright (By Microsoft) (For type checking)
    4. Liveserver (For viewing coverage report html file)


## Setting up python env
* Setup python env w/ following command
    1. create virtual env: `python -m venv .venv`
    2. activate env:
        ```shell
        .venv\Scripts\activate # use this for windows with cmd
        source .venv\Scripts\activate # use this for windows with git bash
        source .venv/bin/activate # use this for linux
        ```
    4. Install pytest & pytest-cov
        ```bash
        pip install pytest pytest-cov
        ```
    3. Select the python interpreter
        * Use: <Ctrl> + <Shift> + P -> Python: Select Interpreter
        * Select `./venv/Scripts/activate`

## Some examples of ruff & pyrights capabilities
1. Formatting the python files
    * Use: <Ctrl> + <Shift> + P -> Ruff: format documents
2. Sorting import statements
    * Use: <Ctrl> + <Shift> + P -> Ruff: format imports
3. Fixing all auto-fixable linting errors with ruff:
    * Use: <Ctrl> + <Shift> + P -> Ruff: fix auto-fixable imports
4. Code Diagnostics Examples:
    * demo.py
        * Diagnostics
        * Hover Hints / Tooltips
        * Quick Fixes / Code Actions

## Configure Tests on VSCode
* Use: <Ctrl> + <Shift> + P -> Python: Configure Tests
* Select testing tool: Choose `pytest`
* Select tests directory: Choose `tests`

## Running Tests
1. Run all tests
    * Use: <Ctrl> + <Shift> + P -> Test: Run all tests
2. Running unit tests on a single file:
    * Use: <Ctrl> + <Shift> + P -> Test: Run tests in current file
3. Running a single function test:
    * Click on the checkmark/error symbol on the gutter.
    OR
    * Use: <Ctrl> + <Shift> + P -> Test: Run test at cursor

## Running tests with command line tool
1. If you want full coverage report w/ html file:
    * Activate your virtual env
    * Run this command: `pytest -s --cov-report=html`
    * Open the index.html file in the generated htmlcov folder
    * Use LiveServer Extension to serve the index.html file.
2. Ignoring pytest config from pyproject.toml file:
    * add `-c NULL` -> `pytest -c null`
3. Running a specific test with pattern matching
    * `pytest -c NULL -k your_pattern`

