import pyperclip
import webbrowser
import requests
import json
import pypkg

class sakurapkgFileCreationError(Exception):
    "The sakurapkg Permission Error Class."

class sakurapkgError(Exception):
    "The sakurapkg Error Class."

class sakurapkg_error():
    def report_error(version, traceback, command):
        resp = requests.get("https://pypi.org/pypi/sakurapkg/json")
        json = resp.json()
        latest_version = json["info"]["version"]
        pyperclip.copy(f'Oops! It looks like some error occurred and the command execution failed. Below is the error information.\nversion:{version}(Latest version is {latest_version})\nThe following error occurred when I executed the command "{command}".\nError: {traceback}')
        print(f"The following content was copied to the clipboard.\n-------------------------------------\n{pyperclip.paste()}\n-------------------------------------")
        yn = input("Do you want to open sakurapkg's github in your web browser? (y/n):")
        if yn == "y":
            webbrowser.open(url="https://github.com/sakurapkg/sakurapkg/issues")
        elif yn == "Y":
            webbrowser.open(url="https://github.com/sakurapkg/sakurapkg/issues")
        else:
            pass