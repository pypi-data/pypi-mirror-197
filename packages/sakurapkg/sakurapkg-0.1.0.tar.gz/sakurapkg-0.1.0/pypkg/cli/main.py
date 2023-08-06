from pypkg.cli.exceptions import PyPkgError, PyPkgFileCreationError
import os, platform
import logging
from cleo import application
from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option
from pypkg.cli.add import add_package_requies
from pypkg.cli.install import install_and_add_package_requies
from pypkg.cli.init import pyinit
from pypkg.cli.about import about
from pypkg.cli.chenge_version import chenge_version

logger = logging.getLogger(__name__)
logging.basicConfig()

COMMANDS = [
    "run",
    "about",
    "add",
    "build",
    "init",
    "change-version",
# Debug Only CMD
    "debug showinfo",
]

def main():
    application = Application()
    application.add(add_package_requies())
    application.add(install_and_add_package_requies())
    application.add(pyinit())
    application.add(about())
    application.add(chenge_version())
    application.run()

if __name__ == "__main__":
    main()
