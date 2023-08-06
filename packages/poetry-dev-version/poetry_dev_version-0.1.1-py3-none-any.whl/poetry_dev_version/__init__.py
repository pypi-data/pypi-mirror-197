try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

from importlib.metadata import PackageNotFoundError

from poetry.plugins.application_plugin import ApplicationPlugin

from .command import DevVersionCommand

__all__ = ["DevVersionCommand", "__version__"]

try:
    __version__ = importlib_metadata.version(__name__)
except PackageNotFoundError:
    __version__ = "0.1.0"


def factory() -> DevVersionCommand:
    return DevVersionCommand()


class DevVersionPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("dev-version", factory)
