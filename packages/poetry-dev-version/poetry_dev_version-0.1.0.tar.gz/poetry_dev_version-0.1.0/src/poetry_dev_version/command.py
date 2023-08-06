from __future__ import annotations

from typing import TYPE_CHECKING, Any, MutableMapping, cast

from cleo.exceptions import CleoValueError
from cleo.helpers import argument, option
from poetry.console.commands.command import Command
from poetry.core.version.exceptions import InvalidVersion
from poetry.core.version.pep440.segments import (
    RELEASE_PHASE_ID_ALPHA,
    RELEASE_PHASE_ID_BETA,
    RELEASE_PHASE_ID_DEV,
    RELEASE_PHASE_ID_RC,
    ReleaseTag,
)
from tomlkit.toml_document import TOMLDocument

if TYPE_CHECKING:
    from poetry.core.constraints.version import Version


class DevVersionCommand(Command):
    name = "dev-version"
    description = "Bumps version when a valid."

    arguments = [
        argument(
            "level",
            "The version level.",
            optional=False,
        ),
        argument(
            "build_number",
            "The version level.",
            optional=False,
        ),
    ]
    options = [
        option("short", "s", "Output the version number only"),
        option(
            "dry-run",
            None,
            "Do not update pyproject.toml file",
        ),
        option(
            "local",
            None,
            "Add local string",
        ),
    ]

    help = """\
The development version command bumps the version of
the project and writes the new development version
back to <comment>pyproject.toml</>.

The new development version should ideally be a valid
semver string or a valid bump rule:
rc, alpha, beta, dev.
"""

    RESERVED = {"rc", "alpha", "beta", "dev"}

    def handle(self) -> int:
        level: str = self.argument("level")

        if level not in self.RESERVED:
            raise CleoValueError(f"Unknown level: {level}")

        try:
            build_number: int = int(self.argument("build_number"))
        except ValueError:
            raise CleoValueError(f"Invalid build number: {self.argument('build_number')}")

        version = self.set_development_version(level=level, build_number=build_number, local=self.option("local"))

        if self.option("short"):
            self.line(version.to_string())
        else:
            self.line(
                "Bumping version from" f" <b>{self.poetry.package.pretty_version}</>" f" to <fg=green>{version}</>"
            )

        if not self.option("dry-run"):
            content: dict[str, Any] = self.poetry.file.read()
            poetry_content = cast(MutableMapping[str, MutableMapping[str, Any]], content["tool"])["poetry"]
            poetry_content["version"] = version.text

            assert isinstance(content, TOMLDocument)
            self.poetry.file.write(content)

        return 0

    def set_development_version(
        self,
        *,
        level: str,
        build_number: int,
        local: str | None = None,
        current_version: str | None = None,
    ) -> Version:
        from poetry.core.constraints.version import Version

        map = {
            "rc": RELEASE_PHASE_ID_RC,
            "alpha": RELEASE_PHASE_ID_ALPHA,
            "beta": RELEASE_PHASE_ID_BETA,
            "dev": RELEASE_PHASE_ID_DEV,
        }

        try:
            parsed = Version.parse(current_version or self.poetry.package.pretty_version)
        except InvalidVersion:
            raise ValueError("The project's version doesn't seem to follow semver")

        if level in {"rc", "alpha", "beta"}:
            new = parsed.replace(pre=ReleaseTag(map[level], build_number))
        else:
            new = parsed.replace(dev=ReleaseTag(map[level], build_number))

        if local:
            if "." in local:
                local_tuple: tuple[str | int, ...] = tuple(local.split(".", 1))

            else:
                local_tuple = (local,)
            new = new.replace(local=local_tuple)

        return new
