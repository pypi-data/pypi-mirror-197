import toml
from cleo.commands.command import Command
from cleo.helpers import argument, option
from pypkg.core import sysinfo

class about(Command):
    name = "about"
    description = "about command"

    def handle(self):
        print("-----------pypkg about------------")
        print(f"version: {sysinfo.version()}")
        print("Developers :{")
        print("     'all' : 'sonyakun'")
        print("}")
        print("----------------------------------")