from pathlib import Path
from shutil import rmtree

from devi.log import deviprint, DEVI_COLORS
from devi.utils import ask_user_input
import devi.config as config

def remove_template(template_name: str, confirm: bool):
    """Remove a template listed on $DEVI_HOME/templates by its name
    """
    name_color = DEVI_COLORS['primary']

    # Here, devi home MUST exist, (see devi.config.init)
    templates = list(Path(config.DEVI_TEMPLATES).iterdir())

    found = next((t for t in templates if t.name == template_name), None)

    if not found:
        deviprint.err(f"template {name_color(template_name)} doesn't exist")
        exit(0)

    if not confirm:
        try:
            deviprint.info(f'template {name_color(template_name)} will be deleted')
            confirm = ask_user_input('enter to remove, ctrl+c to cancel') == ''
        except KeyboardInterrupt:
            deviprint()
            deviprint.success('canceled')
            exit(0)

    if confirm:
        rmtree(found)
        deviprint.success('removed')
        exit(0)
