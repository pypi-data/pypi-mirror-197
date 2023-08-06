# docker-minecraft-cli, a wrapper to install a Minecraft server under Docker.
# Copyright (C) 2023 osfanbuff63
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""docker-minecraft-cli, a wrapper to install a Minecraft server under Docker."""

import platform
import sys
from pathlib import Path

import click

from . import lib

__version__ = "0.2.0"


@click.command(
    help="Run a Minecraft server with Docker in one command. Visit https://docker-minecraft.osfanbuff63.tech/usage for extended help."
)
@click.option(
    "--version", "-V", "version", is_flag=True, help="Show the version and exit."
)
@click.option(
    "--memory",
    "-m",
    "memory",
    default="2G",
    show_default=True,
    help="How much memory to allocate, in the format `nG`, where `n` is an integer.",
)
@click.option(
    "--mc-version",
    "-v",
    "mc_version",
    default="LATEST",
    show_default=True,
    help="The version of Minecraft to use. Any version of Minecraft is acceptable, as well as LATEST (the latest version) or SNAPSHOT (the latest snapshot).",
    required=True,
)
@click.option(
    "--variant",
    "-a",
    "variant",
    help="The variant of the Docker image to use. Valid variants can be found at https://github.com/itzg/docker-minecraft-server#running-minecraft-server-on-different-java-version",
)
@click.option(
    "--type",
    "-t",
    "type",
    help="The type of server. Can be Forge, Fabric, Quilt, Bukkit/Spigot/Paper/Pufferfish/Purpur, you name it. Full list at https://github.com/itzg/docker-minecraft-server#server-types",
    required=True,
)
@click.option("--run/--no-run", "run", help="Create and run this container now.")
@click.option(
    "--container-id",
    "-c",
    "container_id",
    help="An existing container ID. This is given to you if you use --no-run, or in Docker Desktop if you have that installed.",
)
@click.option(
    "--interactive/--no-interactive",
    "-i",
    "interactive",
    help="Emulates the -it option of `docker run`. **This downloads the Docker CLI itself instead of calling through Python** for technical reasons. \nYou probably want this for a new server.",
)
@click.option(
    "--config-init",
    "config_init",
    help="Initializes a config file with the default values. Takes the argument for the path to the config file.",
)
@click.option(
    "--config",
    "-C",
    help="The path to the config file to use. This is not used if --config-init is passed.",
    default="",
)
def docker_minecraft(
    version,
    memory,
    mc_version,
    variant,
    type,
    run,
    container_id,
    interactive,
    config_init,
    config,
):
    """Run a Minecraft server with Docker in one command.
    Visit https://docker-minecraft.osfanbuff63.tech/usage for extended help.
    """
    if version:
        click.echo(f"docker-minecraft-cli {__version__}")
        sys.exit(0)
    config = lib.Config()
    if config_init == "" or config_init:
        click.echo("Initializing config, as --config-init was passed.")
        config_path = Path(config_init).expanduser().resolve()
        file = config.set_file(config_path).format("\\", "/")
        config.init()
        click.echo(f"Config file initialized. Path to the config file: {file}")
        sys.exit(0)
    click.echo("Preparing Docker.")
    client = lib.__init__()
    if container_id:
        click.echo("Container ID passed, using that.")
        container = lib.init_existing(container_id, client)
        if interactive is not True:
            lib.run_existing(container)
            sys.exit(0)
    if not container_id:
        type_str = str(type)
        environment = {
            "EULA": "true",
            "MEMORY": memory,
            "VERSION": mc_version,
            "TYPE": type_str.upper(),
        }
        click.echo("Creating container. This could take a while...")
        container = lib.create(client, environment, variant)
        click.echo("Container created!")
        if interactive is True:
            pass
        elif run is not True:
            click.echo(f"\nContainer ID: {container.id}")
            click.echo(
                "Copy the above ID now, you will need it to run this container later."
            )
            click.echo("This isn't super sensitive, but keep it in a safe place.")
            click.echo(
                "If you don't copy it, just run this command again and it will generate a new one."
            )
            click.echo(
                "You can run this container later with the --container-id option."
            )
            sys.exit(0)
    if interactive is True:
        if config.read()["config"]["interactive_override"] != "true":
            click.echo(
                "This requires downloading the Docker CLI binary and running it."
            )
            click.echo("Are you OK with this?")
            click.echo(
                "(Options: o for OK, s for OK and save my preference, n or no input for no)"
            )
            user_input = input("Option: ")
            if user_input == "o":
                pass
            elif user_input == "s":
                config.write("interactive_override", "true")
            else:
                click.echo("Selected no, exiting.")
                sys.exit(1)
        else:
            click.echo("Found saved preference, skipping interactive question.")
        click.echo("Continuing.")
        cli_file_name = "docker{}"
        if platform.system() == "Windows":
            path = Path(".").resolve() / "docker" / cli_file_name.format(".exe")
        else:
            path = Path(".").resolve() / "docker" / cli_file_name.format("")
        if path.exists() is False:
            click.echo("Docker CLI binary not found, downloading.")
            path = lib.get_docker_cli()
        click.echo("Running container interactively!")
        lib.run_interactive(container, path)
        sys.exit(0)

    click.echo("Running container!")
    lib.run_existing(container)
