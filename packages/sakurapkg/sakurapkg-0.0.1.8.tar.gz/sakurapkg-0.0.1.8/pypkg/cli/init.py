from cleo.commands.command import Command
from cleo.helpers import argument, option
import os
from pypkg.cli.exceptions import PyPkgError, PyPkgFileCreationError
import os, platform
import logging

class pyinit(Command):
    name = "init"
    description = "create pyproject.toml"
    
    def handle(self):
        try:
            print("This utility will walk you through creating a pyproject.toml file.\nIt only covers the most common items, and tries to guess sensible defaults.\n\nSee `pyinit help` for definitive documentation on these fields\nand exactly what they do.\n\nUse `pyinit install <pkg>` afterwards to install a package and\nsave it as a dependency in the pyproject.toml file.\n\nPress ^C at any time to quit.")
            packagename = input("package name:")
            ver = input("version: (1.0.0)")
            des = input("description:")
            homepage = input("homepage:")
            repository = input("repository:")
            author = input("author: yourname <email>")
            pack_license = input("license: (MIT)")
            try:
                if os.path.isfile("pyproject.toml"):
                    raise PyPkgError("A pyproject.toml already exists.")
                else:
                    f = open('./pyproject.toml', 'w')
                    f.write(f'[build-system]\nrequires = ["setuptools", "setuptools_scm"]\nbuild-backend = "setuptools.build_meta"\n[project]\nname = {packagename}\ndescription = {des}\nauthors = [{author}]\nhomepage = {homepage}\nrepository = {repository}\nlicense = {pack_license}\nclassifiers = [\n    "Programming Language :: Python :: 3",\n]\ndynamic = ["version"]\n\n[tool.setuptools.packages.find]\nexclude = ["build", "tests"]')
                    f.close()
                    print("Creation of pyproject.toml is complete.")
            except PermissionError as Pe:
                raise PyPkgFileCreationError("No Authority to create or write files.")
        except KeyboardInterrupt as k:
            logging.warning('init canceled')