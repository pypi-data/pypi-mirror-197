import toml
from cleo.commands.command import Command
from cleo.helpers import argument, option
import logging, os
import subprocess

logger = logging.getLogger(__name__)
logging.basicConfig()

class chenge_version(Command):
    name = "change-version"
    description = "change version"
    options = [
        option(
            "testing",
            "t",
            description="install testing version sakurapkg",
            flag=True
        ),
        option(
            "release",
            "r",
            description="install testing version sakurapkg",
            flag=True
        )
    ]

    def handle(self):
            if self.option("testing"):
                subprocess.Popen("pip install git+https://github.com/sakurapkg/sakurapkg@Testing", shell=True)
            elif self.option("release"):
                subprocess.Popen("pip install sakurapkg", shell=True)
            else:
                pass
