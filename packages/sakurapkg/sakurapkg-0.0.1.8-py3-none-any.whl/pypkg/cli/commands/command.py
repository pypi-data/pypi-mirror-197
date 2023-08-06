from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from cleo.commands.command import Command as BaseCommand
from cleo.exceptions import CleoValueError


class Command(BaseCommand):
    loggers: list[str] = []


    @property
    def pyinit(self) -> pyinit:
        if self._pyinit is None:
            return self.get_application().pyinit

        return self._pyinit

    def set_pyinit(self, pyinit: pyinit) -> None:
        self._pyinit = pyinit

    def get_application(self) -> Application:
        from poetry.console.application import Application

        application = self.application
        assert isinstance(application, Application)
        return application

    def reset_poetry(self) -> None:
        self.get_application().reset_poetry()

    def option(self, name: str, default: Any = None) -> Any:
        try:
            return super().option(name)
        except CleoValueError:
            return default