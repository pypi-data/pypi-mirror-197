from pathlib import Path
from shutil import copy
import subprocess
import tempfile

import devi.config as config
from devi.log import deviprint
from devi.toml_parser import tomllib

class DeviError(Exception):
    """Base class for exceptions in this module."""
    pass

class DeviErrorEditorNotFound(DeviError):
    """User can defined its own editor for devi"""
    pass

class DeviErrorInvalidConfigFile(DeviError):
    """Thrown when the a toml config file was failed to parse"""
    pass

def edit_file(file_path: Path):
    """Opens the file with the default text editor.

    It uses config variable 'DEVI_DEFAULT_EDITOR'
    """
    try:
        subprocess.run([config.DEVI_DEFAULT_EDITOR, file_path], check=True)
    except FileNotFoundError:
        # the editor does not exist
        raise DeviErrorEditorNotFound()

def edit_tmp_file():
    tempfile.mkstemp()

def copy_dir_content(src_path: Path, dest_path: Path):
    """Copies recursively the content of a directory to another.

    dest_path should exist, otherwise this function will create it if no parents
    are needed. Otherwise, will raise FileNotFoundError error from Path.mkdir().
    """
    if not dest_path.exists():
        dest_path.mkdir(exist_ok=True, parents=False)
    if not dest_path.is_dir():
        raise RuntimeError(f'Destination path {dest_path.resolve()} is not a directory')
    if not src_path.is_dir():
        raise RuntimeError(f'Source path {src_path.resolve()} is not a directory')
    for item in src_path.iterdir():
        if item.is_dir():
            # print(f'\ncopying dir content from {(item).absolute()} to {Path(dest_path, item.name).absolute()}')
            # Call it recursively
            copy_dir_content(item, Path(dest_path, item.name))
        else:
            # print(f"copying just a file: {item.absolute()} to {dest_path.absolute()}")
            copy(item, dest_path, follow_symlinks=True)

def ask_user_input(prompt: str, default: str = ""):
    if default:
        deviprint.info(f'{prompt}: ({default}) ', end='')
    else:
        deviprint.info(f'{prompt}: ', end='')

    response = input()

    return response if response else default

def read_config_file(config_file: Path):
    """Open and parse a toml config file

    If it fails to parse the content, throws DeviErrorInvalidConfigFile
    It raise `open` errors like IOError
    Equivalent to tomllib.load(open(config_file, 'rb'))
    """
    try:
        with open(config_file, 'rb') as conf:
            return tomllib.load(conf)
    except tomllib.TOMLDecodeError as e:
        raise DeviErrorInvalidConfigFile(e)
    except Exception:
        raise
