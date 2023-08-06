from typing import Any

import click
from pulp_glue.common.i18n import get_translation
from pulpcore.cli.common.generic import pulp_group

from pulpcore.cli.maven.distribution import distribution
from pulpcore.cli.maven.remote import remote
from pulpcore.cli.maven.repository import repository

translation = get_translation(__name__)
_ = translation.gettext

__version__ = "0.2.0"


@pulp_group(name="maven")
def maven_group() -> None:
    pass


def mount(main: click.Group, **kwargs: Any) -> None:
    maven_group.add_command(repository)
    maven_group.add_command(remote)
    maven_group.add_command(distribution)
    main.add_command(maven_group)
