from pathlib import Path

from devi.toml_parser import tomllib
from devi.log import deviprint, ANSIcodes, DEVI_COLORS
import devi.config as config

def list_templates():
    """List all the available templates in $DEVI_HOME/templates.

    It will show the 'description' field in the template.devi.toml file
    if defined. If the 'name' field is not defined, will use the dir name.
    """
    name_color = DEVI_COLORS['primary']
    mark_color = DEVI_COLORS['secondary']

    print(DEVI_COLORS['secondary'](config.DEVI_TEMPLATES.as_posix()))

    # Here, devi home MUST exist, (see devi.config.init)
    templates = list(Path(config.DEVI_TEMPLATES).iterdir())

    if len(templates) == 0:
        deviprint(mark_color('└──'))
        deviprint()
        deviprint.info(f"is kind of empty here, try {ANSIcodes.underline}{DEVI_COLORS['primary']('devi add')}")
        exit(0)

    last_template = templates[-1].name

    # To store templates that are not directories (invalid templates)
    not_dirs = []

    # Display the directory tree (non-recursive)
    for template in templates:
        template_config_path = template / config.DEVI_TEMPLATE_TOML_FILENAME

        mark = mark_color("├──" if template.name != last_template else "└──")
        deviprint(f'{mark} {name_color(template.name)}' + ANSIcodes.reset, end='')

        if not template.is_dir():
            not_dirs.append(template.name)
        if not template_config_path.exists():
            continue

        # Exists, so try to get the description
        try:
            with open(template_config_path, 'rb') as conf_file:
                description = tomllib.load(conf_file).get('description')
                # Print the template information
                deviprint(f' - {description}' if description else '')
        except (IOError, tomllib.TOMLDecodeError) as e:
            deviprint.err(f'Error reading {template_config_path}\n{e}')
            continue

    if (how_many := len(not_dirs)) > 0:
        deviprint()
        not_dirs_str = DEVI_COLORS['warning'](str(not_dirs))
        deviprint.warn(f"watch out: {not_dirs_str} {'are not directories' if how_many > 1 else 'is not a directory'}")
        deviprint.warn('you should delete it')
