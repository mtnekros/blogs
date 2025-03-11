# UV Package Manger Notes

## Creating a project
* cmd: `uv init project_name`
    * it will create some default files
        * empty README.md
        * pyproject.toml file
            * with project names & dependencies
            * python version etc
        * a main.py file

* Stores dependencies in a pyproject.toml file
* Stores strict versioning in uv.lock

## Handling dependencies
* Adding package:
    * cmd: `uv add package_name`
* Removing package:
    * cmd: `uv remove package_name`
* Upgrading packages
    * cmd: `uv lock --upgrade-package package_name`

## Running Commands:
* Running python files:
    * cmd: `uv run script.py` for `python script.py`
* Running any python commands:
    * cmd: `uv run -- flask run -p 3000`

## Update python virtual env
* Creating a virtual env based on the lock file/dependencies
    * cmd: `uv sync`
        * will create .venv folder & install all dependencies there.
* We can activate like a normal virtualenv
    * cmd: `.\.venv\Scripts\activate`
        * or just use `uv run` prefix to run any files 
        * or use `uv run -- cmd` to run any command

## Tools in UV
* Examples of tools:
    * ruff (linter)
    * cowsay (cow says things)
    * httpie (like cURL but with better default options)
* running the tool
    * uv run tool ruff
    * uv run tool cowsay
    * uv run tool pytest

## UVX
* `uvx` is another command that is used to run tools without installing it
  directly to current virtual environment. It installs it in a isolated
  environment and you can run the tools using following command.
    * cmd: `uvx cowsay hello diwash` instead of `uv run tool cowsay`
* it's possible to specify versions & git repos to get the tool/packages
  from as well with --from options
    * cmd: `uvx --from 'ruff==0.3.0' ruff check`
        or
    * cmd: `uvx --from git+https://github.com/httpie/cli httpie`

## Installing python with uv
* you can install different versions of python using uv
    * cmd: `uv python install 3.12`
        * works like a charm in a windows machine too. Which doesn't happend with pyenv
* you can even install different implementations of python
    * cmd: `uv python install pypy@3.10`
* reinstalling python:
    * cmd: `uv python install --reinstall`
* listing installed python versions:
    * cmd: `uv python list`
* it will also automatically download python if required by some commands
    * cmd: `uvx python@3.12 -c "print('hello world')"
    * cmd: `uv venv venv`
        * creating virtual environment with uv

