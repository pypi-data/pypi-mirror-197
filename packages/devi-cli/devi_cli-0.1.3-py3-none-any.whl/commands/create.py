import sys
import subprocess
from pathlib import Path
from shutil import rmtree
from typing import Optional

from devi.utils import (
    copy_dir_content, read_config_file, DeviErrorInvalidConfigFile
)
from devi.log import deviprint, DEVI_COLORS
import devi.config as config

if not config.is_windows:
    import fcntl, termios

def create_project(
    template_name: str,
    destination:   Optional[str] = None,
    project_name:  Optional[str] = None
):
    """Create a project from an existing template"""
    template_dir = Path(config.DEVI_TEMPLATES, template_name)

    # Check if the template indeed exists
    if not template_dir.exists():
        colored_name = DEVI_COLORS['primary'](f"'{template_name}'")
        deviprint.err(f"Template {colored_name} does not exist")
        exit(1)

    # Read the template.devi.toml file
    conf_data: dict = {}
    devi_conf_file = template_dir / config.DEVI_TEMPLATE_TOML_FILENAME
    try:
        conf_data = read_config_file(devi_conf_file)
    except FileNotFoundError as e:
        pass
    except IOError as e:
        deviprint.err(f'error reading {devi_conf_file}:\n{e}')
        exit(1)
    except DeviErrorInvalidConfigFile as e:
        deviprint.err(f'Cannot parse your {devi_conf_file}: \n{e}')
        deviprint.err('aborting')
        exit(1)

    # Prefer: name in flag -> name in config -> template name
    name_to_create = project_name or conf_data.get('name', template_name)

    # Prefer: destination in flag -> destination in config -> error
    destination_to_create = destination or conf_data.get('destination', None)
    if not destination_to_create:
        deviprint.err(
            f"{DEVI_COLORS['primary']('destination')} is defined in {DEVI_COLORS['primary']('template.devi.toml')}, use --dest"
        )
        exit(1)
    # TODO: what if is not an string? maybe is better to validate first the whole config file

    destination_path = Path(destination_to_create).expanduser()

    if not destination_path.exists():
        deviprint(f'{destination_path} Does not exist, creating')
        destination_path.mkdir(parents=True, exist_ok=True)
    if not destination_path.is_dir():
        deviprint.err(f'invalid destination: {destination_path} (not a directory)')
        exit(1)

    new_project_dir = Path(destination_path, name_to_create)
    if new_project_dir.exists():
        deviprint.err(f"couldn't create project in {DEVI_COLORS['primary'](new_project_dir.resolve().as_posix())} (already exists)")
        exit(1)

    # Copying content and then executing the oncreate command if defined
    copy_dir_content(template_dir, new_project_dir)
    deviprint.success(f"created {DEVI_COLORS['primary'](name_to_create)} at \'{new_project_dir.resolve()}\'")

    oncreate_cmd = conf_data.get('oncreate', None)
    if oncreate_cmd:
        deviprint.info(f"running {DEVI_COLORS['secondary']('oncreate')} command:")
        deviprint(f'> {oncreate_cmd}')
        # Run the command and pipe the stdout and stderr to this process
        output = subprocess.run(oncreate_cmd,
            shell=True, cwd=new_project_dir,
            stdout=sys.stdout, stderr=sys.stderr
        )
        if output.returncode != 0:
            deviprint.err(f"{DEVI_COLORS['secondary']('oncreate')} command failed with code {output.returncode}")
            deviprint.err('project was not created')
            rmtree(new_project_dir)
            exit(output.returncode)

    # Remove all the *.devi.* files/directories from the created project
    # (see README)
    for f in new_project_dir.rglob('*.devi.*'):
        if f.is_dir():
            rmtree(f)
        else:
            f.unlink()

    wanna_change_dir = conf_data.get('change_dir', False)
    if wanna_change_dir:
        if config.is_windows:
            deviprint.warn('warning: `change_dir` is not implemented yet on Windows')
            exit(0)

        dir_to_change = new_project_dir.resolve().as_posix()
        cmd = f"cd {dir_to_change}\n"
        for c in cmd:
            fcntl.ioctl(sys.stdin, termios.TIOCSTI, c.encode())
