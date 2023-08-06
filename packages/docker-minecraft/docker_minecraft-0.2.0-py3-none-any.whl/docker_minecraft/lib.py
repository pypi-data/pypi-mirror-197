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
"""Utility functions and classes."""

import hashlib
import os
import platform
import random
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Union

import requests
import tomlkit
from docker.errors import APIError  # type: ignore
from docker.models.containers import Container  # type: ignore
from tomlkit import toml_file

import docker  # type: ignore
from docker import DockerClient  # type: ignore


class DockerError(Exception):
    """A generic error occurred from Docker."""


class UnreachableServerError(DockerError):
    """The Docker server was unreachable."""


class InvalidValue(Exception):
    """The value was invalid."""


class HashError(OSError):
    """The hash of the file was invalid."""


class Config:
    """Configuration support."""

    def __init__(
        self,
        file: Union[str, bytes, os.PathLike] = Path("~").expanduser()
        / ".config"
        / "docker_minecraft.toml",
    ):
        global file_str
        # (this isn't an issue)
        file_str = str(file)  # type: ignore

    def init(self):
        """Initialise the config file with the default values.
        This should **only** be run if the config file does not exist, as it will delete the file
        if it already exists, which will overwrite any user-set settings - which you don't want to do for obvious reasons.
        """
        config_file = tomlkit.document()
        # TODO: Add actual docs and URL for this
        config_file.add(
            tomlkit.comment("Read more about this file at <insert_wiki_url>")
        )
        config_file.add(tomlkit.nl())

        config = tomlkit.table()
        config.add("interactive_override", True)

        config_file.add("config", config)
        file = toml_file.TOMLFile(file_str)
        try:
            file.write(config_file)
        except FileExistsError:
            os.remove(file)
            file.write(config_file)

    def set_file(self, file: Path) -> str:
        """Set the file to use globally."""
        file_str = str(file)
        return file_str

    def read(self) -> dict:
        """Read from the config file.

        Returns:
            dict: The config file, reformatted into a dict-like format.
        """
        # this isn't an issue
        config_file = toml_file.TOMLFile(file_str)  # type: ignore
        try:
            return config_file.read()
        except FileNotFoundError:
            self.init()
            return config_file.read()

    def write(self, key: str, value: str) -> None:
        """Write to the config file.
        This is a mostly internal function used to write to the config file from a user interface.

        Args:
            key (str): The key to write to.
            value (str): The value to write to `key`.
        """
        config_file = self.read()
        try:
            # as this is the only category we use right now, this is hardcoded
            config_file["config"][key]
        except KeyError as exception:
            raise KeyError("Invalid key.") from exception
        # read 5 lines above
        config_file["config"][key] = value
        toml_file.TOMLFile(file_str).write(config_file)  # type: ignore


def _get_docker_cli() -> str:
    """Get the Docker CLI binary and return the path to it.
    This doesn't check whether it exists already - don't run this function without that check.
    """
    url_placeholder = (
        "https://download.docker.com/{}/static/stable/{}/docker{}-23.0.1.{}"
    )
    if platform.system() == "Windows":
        if platform.machine().startswith("arm") or platform.machine().startswith(
            "aarch"
        ):
            raise InvalidValue("Docker builds don't exist for this architecture.")
        url = url_placeholder.format("win", "x86_64", "", "zip")
        compress_type = "zip"
    elif platform.system() == "macOS":
        if platform.machine().startswith("arm") or platform.machine().startswith(
            "aarch"
        ):
            url = url_placeholder.format("mac", "aarch64", "", "tgz")
        else:
            url = url_placeholder.format("mac", "x86_64", "", "tgz")
        compress_type = "gztar"
    elif platform.system() == "Linux":
        if platform.machine().startswith("arm") or platform.machine().startswith(
            "aarch"
        ):
            url = url_placeholder.format("linux", "aarch64", "rootless-extras", "tgz")
        else:
            url = url_placeholder.format("linux", "x86_64", "rootless-extras", "tgz")
        compress_type = "gztar"
    else:
        raise InvalidValue("Your operating system is unsupported.")
    response = requests.get(url)
    if response.status_code == 200:
        _extract_compressed(response, ".", compress_type)
    path = "."
    cli_file_name = "docker{}"
    if platform.platform().startswith("Windows"):
        cli_path = str(Path(path).resolve() / "docker" / cli_file_name.format(".exe"))
    else:  # Assuming POSIX-compliant environment (?)
        cli_path = str(Path(path).resolve() / "docker" / cli_file_name.format(""))
    return cli_path


def _extract_compressed(
    response: requests.Response,
    path: Optional[Union[str, os.PathLike[str]]],
    file_type: str,
) -> None:
    """Download and extract the binary, checking the SHA256 hash on the way."""
    tmp_file = f"docker.{file_type}"
    with open(tmp_file, "wb") as temp_file:
        for chunk in response.iter_content():
            temp_file.write(chunk)
    expected_hashes = [
        "3c8258175c5b666e3d1b96d78e37984619e072b3228a76388177bbeb74c7f82d",
        "2ee26389a9edc59dfa0029c4fd2b79fa15b87943219860302e954660dc63c8c0",
        "09c3d2789db3d20f8429b9c4d56c9e2307229777db8347eb4a5d2c5405e77efb",
        "8d116b00d99a4cfe6560215ba204df73f63f059d5ad9260983900584c7708918",
        "e1cd34abdb401fad563171164cdfd5f5dd1ebf1b1905edfae20fb61cc7339eab",
    ]
    _check_docker_sha(tmp_file, expected_hashes)
    shutil.unpack_archive(tmp_file, path)
    os.remove(tmp_file)


def _check_docker_sha(
    file: Union[str, bytes, os.PathLike],
    expected_hashes: list = [
        "3db7922c6a88c8dd09ece552b3794fa390776e842829c7b7aa3e8f6f54565792",
        "7d8ece38aa695109f0ee71f26952ee1dffaedd1025f745f2f4dbf7bbd09710ad",
        "55ba0ba8e239ff227478d4cd128221646a8842ccf495053b006e94965b3999da",
        "5bf1dbd84b82269bbc55d5f12fe61f3fc35caa38762ce752ae8fe1afd18f8700",
        "b492bfac1ae71b984c713dd090f6926ff5cf670bbf26f19590880136596b9a7e",
    ],
):
    """Gets the SHA256 hash of the file and checks it to a list of potential hashes."""
    with open(file, "rb") as file_to_hash:
        sha_hash = hashlib.file_digest(file_to_hash, "sha256")
    if sha_hash.hexdigest not in expected_hashes:
        raise HashError("The hash of the file did not match the expected hash.")


def get_docker_cli() -> str:
    """Get the Docker CLI, check the SHA256 hash of it, and return the path to it."""
    file = _get_docker_cli()
    try:
        _check_docker_sha(file)
    except HashError as hash_error:
        raise HashError(
            "The hash of the Docker CLI file was incorrect."
        ) from hash_error
    return file


def __init__() -> DockerClient:
    """Initializes a Docker client."""
    client = docker.from_env()  # type: ignore
    try:
        client.ping()
    except APIError as exc:
        raise UnreachableServerError(
            "The Docker Hub server was unreachable. Are you connected to the Internet?"
        ) from exc
    return client


def create(
    client: DockerClient, environment: dict, variant: Optional[str] = None
) -> Container:
    """Create the Docker container, but don't run it yet.

    Args:
        client (docker.DockerClient): The Docker client to create under.
        environment (dict): The environment variables, to pass to itzg/minecraft-server.
        variant (str, optional): The variant

    Returns:
        Container: The container object.
    """
    if variant is not None:
        if variant not in [
            "latest",
            "java8",
            "java8-multiarch",
            "java8-jdk",
            "java8-openj9",
            "java8-graalvm-ce",
            "java11",
            "java11-jdk",
            "java11-openj9",
            "java17",
            "java17-jdk",
            "java17-openj9",
            "java17-graalvm-ce",
            "java17-alpine",
            "java19",
        ]:
            raise InvalidValue(
                "Invalid variant. Check https://github.com/itzg/docker-minecraft-server#running-minecraft-server-on-different-java-version for a list of valid variants."
            )
        elif (
            variant
            not in [
                "latest",
                "java8-multiarch",
                "java11",
                "java11-jdk",
                "java17",
                "java17-jdk",
                "java17-graalvm-ce",
                "java19",
            ]
            and platform.machine().startswith("arm")
            or platform.machine().startswith("aarch")
        ):
            raise InvalidValue("This value won't work on your CPU.")
    else:
        if environment["VERSION"] == "LATEST" or environment["SNAPSHOT"]:
            pass
        elif environment["VERSION"] < 1.17:
            variant = "java8-multiarch"
        else:
            variant = "latest"
    client.images.pull("itzg/minecraft-server", variant)
    return client.containers.create(
        "itzg/minecraft-server",
        name=f"minecraft-server-{str(random.random())}",
        environment=environment,
        ports={"25565/tcp": "25565"},
        stdin_open=True,
    )


def init_existing(id: str, client: DockerClient) -> Container:
    """Initialize an existing container from the ID.

    Args:
        id (str): The container ID.
        client (docker.DockerClient): The client to register the container under.

    Returns:
        Container: The container that was retrieved.
    """
    container = client.containers.get(id)
    return container


def run_existing(container: Container):
    container.start()
    for line in container.logs(stream=True):
        print(line)


def run_interactive(container: Container, path: Union[str, bytes, os.PathLike]):
    """Run a containter interactively, using the Docker CLI.

    Args:
        container (Container): The container to run
        path (Path-like object): The path to the Docker CLI.
    """
    file_path = str(path)
    try:
        subprocess.run([file_path, "start", "-i", container.id], shell=True)
    except APIError as e:
        raise APIError(
            "The port is already allocated. Is there already a container running?"
        ) from e
