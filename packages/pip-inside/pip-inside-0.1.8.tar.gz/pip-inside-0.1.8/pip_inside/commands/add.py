import os
import shutil
import subprocess
import sys
from typing import Optional

import click
from InquirerPy import inquirer

from pip_inside.utils import misc
from pip_inside.utils.pyproject import PyProject


def handle_add(name: str, group: Optional[str]):
    try:
        if os.environ.get('VIRTUAL_ENV') is None:
            proceed = inquirer.confirm(message='Not in virutal env, sure to proceed?', default=False).execute()
            if not proceed:
                return
        pyproject = PyProject.from_toml()
        name = misc.norm_name(name)
        if pyproject.find_dependency(name, 'main'):
            click.secho("Skip, already installed as main dependency")
            return
        name_installed = pyproject.find_dependency(name, group)
        if name_installed:
            if name_installed == name:
                click.secho("Skip, already installed")
            else:
                pyproject.remove_dependency(name_installed, group)
        cmd = [shutil.which('python'), '-m', 'pip', 'install', name]
        if subprocess.run(cmd, stderr=sys.stderr, stdout=sys.stdout).returncode == 0:
            pyproject.add_dependency(name, group)
            pyproject.flush()
    except subprocess.CalledProcessError:
        pass
