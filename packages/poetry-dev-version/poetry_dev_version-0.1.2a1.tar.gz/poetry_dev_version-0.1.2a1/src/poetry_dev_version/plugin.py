from poetry.plugins.application_plugin import ApplicationPlugin

from .command import DevVersionCommand



def factory() -> DevVersionCommand:
    return DevVersionCommand()


class DevVersionPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("dev-version", factory)
