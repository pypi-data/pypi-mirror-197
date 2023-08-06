import toml
from cleo.commands.command import Command
from cleo.helpers import argument, option
import logging, os
import pypkg
from pypkg.exceptions import sakurapkg_error
from toml.decoder import TomlDecodeError

logger = logging.getLogger(__name__)
logging.basicConfig()

def add_requires(name):
    try:
        if os.path.isfile("pyproject.toml"):
            dict_toml = toml.load(open('pyproject.toml'))
            var = dict_toml['build-system']['requires']
            dict_toml['build-system']['requires'] = var + [name]
            toml.dump(dict_toml, open('pyproject.toml', mode='w'))
        else:
            raise FileNotFoundError("pyinit init not executed (pyproject.toml does not exist).")
    except (TomlDecodeError,TypeError,PermissionError) as e:
        sakurapkg_error.report_error(version=pypkg.__version__, traceback=e, command=f"sakura install {name}")
    

class add_package_requies(Command):
    name = "add"
    description = "pyproject.toml add requiements package"
    arguments = [
        argument(
            "package"
        )
    ]

    def handle(self):
        package = self.argument("package")

        if package:
            add_requires(name=package)
            logging.info("Package Added.")
        else:
            logging.warning("Failed to add package: unknown package name")
