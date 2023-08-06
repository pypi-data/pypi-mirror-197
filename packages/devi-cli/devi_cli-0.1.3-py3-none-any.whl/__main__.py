# rgb 157, 164, 92
devi_bin = f"\u001b[32m{'devi'}\u001b[0m"

__doc__ = f"""{devi_bin}: a tool for managing your project templates

usage:
    {devi_bin} add <path> [<template-name>]
    {devi_bin} create <template-name> [<destination>] [--name=<project-name>]
    {devi_bin} create <template-name> as <project-name> in <destination>
    {devi_bin} list
    {devi_bin} rm     <template-name> [-y]
    {devi_bin} (-h | --help) | --version

options:
    -d, --dest=<destination>    Destination directory for the new project
    -n, --name=<project-name>   Name of the new project
    -h, --help   Shows this screen.
    --version    Shows {devi_bin} version.
"""

if __name__ != "__main__":
    print(f'{devi_bin} is not meant to be imported yet!')

from docopt import docopt
try:
    import devi
    import devi.cli
except ImportError as e:
    print('\nThe following import errors ocurred:\n')
    print(e)
    print(f'\nIf you cloned the project, go to the {devi_bin}\'s root and run:\n')
    print('  pip install -e .')
    print(f'\nto install an editable version of {devi_bin}')
    exit(1)

args = docopt(__doc__, version=devi.__version__, help=True)
devi.cli.main(args)
