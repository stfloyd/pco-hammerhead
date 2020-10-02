PCO Group Type Tagger
======
<a href="#">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" />
</a>

A handy script to apply a tag group to an entire group type in Planning Center Online.
<br/>

## Quick Start
* Enter virtual environment with `pipenv shell`
* Install dependencies by running `pipenv install`
* Run tool with `python main.py`
* 😎 **That's it!**
<br/>

## Project Structure
* All configuration for the program will go in `config/`.
    * `config.json` is the default configuration file.
* `app/`
    * `__init__.py` contains 3 important methods:
        * `init(args)` is the initial configuration stage of the program.
        * `load_config(args)` is the configuration file loading stage.
        * `process(args, config)` is the main logic of the program.
    * `logging.py` defines specialized logging helper definitions.
    * `settings.py` defines program operating settings.
* `config/` contains program JSON configuration files.
* `tests/` contains tests for the project (pytest).
* `logs/` contains program logs (debug, error, default).
* `main.py` is the main entry point of the program.
</br>

## Configuration
See `config/config.example.json` and supply your own credentials/API keys.
</br>

## Commands & Usage
##### This template uses [argparse](https://docs.python.org/3/library/argparse.html) to define CLI commands.
* `-h, --help` prints command and syntax help for the program.
* `-v, --verbose` enables verbose output.
* `-c, --config` point to a non-default configuration file.
* `--version` prints program version information.
##### Example: `python main.py --config=config/secondary.json --verbose`
