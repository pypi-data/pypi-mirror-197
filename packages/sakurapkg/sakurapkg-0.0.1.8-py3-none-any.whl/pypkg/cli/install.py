import toml
from toml.decoder import TomlDecodeError
from cleo.commands.command import Command
from cleo.helpers import argument, option
import logging, os, requests, json, sys, subprocess, re, platform, pathlib
import itertools
import threading
import time
import pypkg
from pypkg.exceptions import sakurapkg_error
logger = logging.getLogger(__name__)
logging.basicConfig()
def loading():
    global done

    done = False
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rinstalling now... ' + c)
        time.sleep(0.1)

def add_requires(name):
    if os.path.isfile("pyproject.toml"):
        try:
            dict_toml = toml.load(open('pyproject.toml'))
            var = dict_toml['build-system']['requires']
            dict_toml['build-system']['requires'] = var + [name]
            toml.dump(dict_toml, open('pyproject.toml', mode='w'))
        except (TomlDecodeError,TypeError,PermissionError) as e:
            sakurapkg_error.report_error(version=pypkg.__version__, traceback=e, command=f"sakura install {name}")
    else:
        raise FileNotFoundError("pyinit init not executed (pyproject.toml does not exist).")

class install_and_add_package_requies(Command):
    name = "install"
    description = "pyproject.toml add requiements package"
    arguments = [
        argument(
            "package"
        )
    ]

    def handle(self):
        package = self.argument("package")
        global done
        if package:
            url = f"https://pypi.org/pypi/{package}/json"
            response = requests.get(url)
            data = response.json()
            py_version = platform.python_version()
            rtext = r"\'.'\'"
            version = re.findall(rtext, py_version)
            print("")
            try:
                data["message"]
                print("Package NotFound.")
            except KeyError:
                if sys.platform == "linux":
                    t = threading.Thread(target=loading)
                    t.start()
                    subprocess.Popen(f"pip install {package}").wait()
                    done = True
                elif sys.platform == "Darwin":
                    t = threading.Thread(target=loading)
                    t.start()
                    subprocess.Popen(f"pip install {package}").wait()
                    done = True
                elif sys.platform == "win32":
                    t = threading.Thread(target=loading)
                    t.start()
                    subprocess.Popen(f"pip install {package}").wait()
                    done = True
                add_requires(name=package)
                logging.info("Package Added.")
        else:
            logging.warning("Failed to add package: unknown package name")
