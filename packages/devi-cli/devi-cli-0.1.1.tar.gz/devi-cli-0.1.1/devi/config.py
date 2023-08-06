import os
import platform
from pathlib import Path
from devi.log import deviprint, DEVI_COLORS
from devi.toml_parser import tomllib
from typing import Callable

is_windows = platform.system() == 'Windows'

DEVI_HOME: Path
DEVI_TEMPLATES: Path
DEVI_CONFIG: Path
DEVI_TEMPLATE_TOML_CONTENT: Callable[[str], str]
DEVI_DEFAULT_EDITOR: str
DEVI_COLORS: dict[str, Callable[[str], str]]

def init():
    """
    Initialize the config variables for devi.
    """
    global DEVI_HOME
    global DEVI_TEMPLATES
    global DEVI_CONFIG

    global DEVI_TEMPLATE_TOML_FILENAME
    global DEVI_TEMPLATE_TOML_CONTENT
    global DEVI_DEFAULT_EDITOR

    global DEVI_COLORS # defined in log.py

    # Default home is ~/.devi
    if (devi_home := os.getenv('DEVI_HOME')) and isinstance(devi_home, str):
        DEVI_HOME = Path(devi_home).expanduser()
    else:
        DEVI_HOME = get_default_devi_home()

    first_time_using_devi = False

    if not DEVI_HOME.exists():
        first_time_using_devi = True

    try:
        # exists ok
        create_devi_home_tree(DEVI_HOME)
        if first_time_using_devi:
            deviprint(DEVI_COLORS)
            deviprint.info(
                f'we created a \'.devi\' dir in \'{DEVI_HOME.resolve().as_posix()}\' just for you!'
            )
            deviprint.info(f"if you want to override it, define {DEVI_COLORS['info']('$DEVI_HOME')}\n")
    except Exception as e:
        deviprint.err(f'couldn\'t create $DEVI_HOME at \'{DEVI_HOME}\'. exiting')
        deviprint.err(f'error received: {e}')
        exit(1)

    # Templates are stored in ~/.devi/templates
    DEVI_TEMPLATES = Path(DEVI_HOME, 'templates')
    # Config file for devi is ~/.devi/config.toml
    DEVI_CONFIG = Path(DEVI_HOME, 'config.toml')

    try:
        with open(DEVI_CONFIG, 'rb') as f:
            conf = tomllib.load(f)
            # loading config options
            DEVI_DEFAULT_EDITOR = conf.get('editor', get_default_text_editor())
    except IOError:
        # deviprint.warn('couldn\'t found devi config')
        DEVI_DEFAULT_EDITOR = get_default_text_editor()
        pass

    DEVI_TEMPLATE_TOML_FILENAME = 'template.devi.toml'
    # Will use this if "DEVI_HOME / DEVI_TEMPLATE_TOML_FILENAME" config file is not defined
    DEVI_TEMPLATE_TOML_CONTENT = lambda template_name: f"""# edit this if you want to change the template name
name = '{template_name}'

# this description will be shown on `devi list`
description = ''

# destination to be used when you create this template with `devi create`
# (can be relative or absolute)
destination = '.'

# command to execute after template creation
oncreate = ''

# wheter you want to 'cd' to the newly created template or not
change_dir = true
"""

def get_default_text_editor() -> str:
    """Try to get the default text editor from the environment variables.

    It falls back for notepad on Windows and
    [sensible-editor, editor, nano, vim, vi] on *nix.
    """
    # prefer VIEWER as sensible-editor does
    for editor in [os.getenv('VIEWER'), os.getenv('EDITOR')]:
        if editor: return editor

    find_cmd = 'where' if is_windows else 'which'
    null = 'NUL' if is_windows else '/dev/null'

    for editor in ['sensible-editor', 'editor', 'nano', 'vim']:
        if os.system(f'{find_cmd} {editor} >{null} 2>&1') == 0:
            return editor

    return 'notepad' if is_windows else 'vi'

def get_default_devi_home() -> Path:
    """Defaults to ~/.devi in *nix and %USERPROFILE%\\.devi in Windows."""
    return Path.home() / '.devi'

def create_devi_home_tree(devi_home: Path):
    """Creates the default devi's tree structure."""
    devi_home.mkdir(parents=True, exist_ok=True)
    (devi_home / 'templates').mkdir(parents=True, exist_ok=True)
