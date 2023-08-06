from os import rename
from sys import exit
from shutil import rmtree
from pathlib import Path
from typing import Optional
from subprocess import CalledProcessError

from devi.utils import (
    copy_dir_content,
    read_config_file,
    edit_file,
    DeviErrorEditorNotFound,
    DeviErrorInvalidConfigFile
)
import devi.config as config
from devi.log import deviprint, DEVI_COLORS

# TODO: convert this to interactive input instead of file editing
# reasons:
# - input validation: currently, we can only validate the input after file was edited
#   - we need to validate if template name already exists
# - better feeling: we are an interactive cli application
def add_template(src_path: Path, template_name: Optional[str]):
    """Main functionality for the devi's `add` command.
    """
    # Default template name is the dir name
    if not template_name:
        template_name = src_path.resolve().name

    if not src_path.exists():
        deviprint.err(f'path \'{src_path}\' does not exist')
        exit(1)

    if not src_path.is_dir():
        deviprint.err(
            f"'{src_path.resolve()}' is not a directory, that's not how templates work"
        )
        exit(1)

    template_path = Path(config.DEVI_TEMPLATES, template_name)

    # We need to handle the case where the template already exists
    if template_path.exists():
        deviprint.err(f"template '{template_name}' already exists")
        exit(1)

    # Copy all the files to $DEVI_HOME / templates
    copy_dir_to_template(src_path, template_name)

    template_config_path = Path(config.DEVI_TEMPLATES, template_name, config.DEVI_TEMPLATE_TOML_FILENAME)

    # The user may have a pre-defined template config, so we need to check that
    if not template_config_path.exists():
        template_config_path.touch()
        dump_default_template_config(template_config_path, template_name)

    # Edit the new config file
    editor = config.DEVI_DEFAULT_EDITOR
    try:
        deviprint.info('opening config in editor...')
        edit_file(template_config_path)
    except CalledProcessError as e:
        deviprint.err(f'{editor} exited with code {e.returncode}')
        exit_cleanup(template_path)
    except DeviErrorEditorNotFound as e:
        deviprint.warn(f"couldn't find editor: '{editor}', do you defined it properly?")

    # Finally, read and parse the config file
    # It is not necesary a "new name", can be the directory same
    new_name = ""
    try:
        conf_data = read_config_file(template_config_path)
        new_name = conf_data['name']
    except DeviErrorInvalidConfigFile as e:
        deviprint.err('failed to parse your config file:')
        deviprint(e)
        exit_cleanup(template_path)
    except FileNotFoundError as e:
        # This shouldn't happen, config file was created previously
        e.add_note('This may happened because the config file that previously existed was deleted')
        exit_cleanup(template_path, only_cleanup=True)
        raise

    # New template name, if modified by the user
    if new_name != template_name:
        if isinstance(new_name, str):
            try:
                template_path.rename(template_path.parent / new_name)
                template_name = new_name
            except Exception as e:
                deviprint.err(f'error when renaming the template name: {e}')
        else:
            deviprint.err('template name must be an string')
            exit_cleanup()

    deviprint.info(f"new template {DEVI_COLORS['primary'](template_name)} created succesfully")

def copy_dir_to_template(src_path: Path, template_name: str):
    template_path = Path(config.DEVI_TEMPLATES, template_name)
    try:
        # This function handles
        copy_dir_content(src_path, template_path)
    except (Exception, KeyboardInterrupt) as e:
        deviprint()
        deviprint.err(f"error copying recusively to '{template_path}': {e}")
        exit_cleanup(template_path)

def dump_default_template_config(template_file: Path, template_name: str):
    """Dumps a default config file for your new templates.

    The default content is defined in the DEVI_TEMPLATE_TOML_CONTENT constant.
    The default name for this config file should be 'default.template.devi.toml',
    and is defined in the DEVI_TEMPLATE_TOML_FILENAME constant.
    """
    conf_str = config.DEVI_TEMPLATE_TOML_CONTENT(template_name)
    try:
        with open(template_file, 'w+') as t_conf:
            t_conf.write(conf_str)
    except (IOError, OSError):
        raise

def exit_cleanup(dir_to_delete: Optional[Path] = None, only_cleanup=False):
    if dir_to_delete:
        rmtree(dir_to_delete, ignore_errors=True)
    deviprint.err('template creation aborted')
    if not only_cleanup:
        exit(1)
