## Transformer

import os
import pathlib
import sys
from typing import TextIO

import yaml

from .commander import CLI, build_cli
from .commanders.typer import TyperCommander
from .manifests import get_cli_manifest

PYTHON_BIN = f"{sys.exec_prefix}/bin"
PYTHON_EXECUTABLE = sys.executable
CLIFFY_CLI_DIR = f"{pathlib.Path(__file__).parent.resolve()}/clis"


class Transformer:
    """Loads command manifest and transforms it into a CLI"""

    def __init__(self, manifest_io: TextIO) -> None:
        self.manifest_io = manifest_io
        self.command_config = self.load_manifest()
        self.manifestVersion = self.command_config.pop('manifestVersion', '')
        self.manifest = get_cli_manifest(self.manifestVersion)(**self.command_config)

    def render_cli(self) -> None:
        self.cli = build_cli(self.manifest, commander_cls=TyperCommander)

    def load_cli(self) -> CLI:
        self.render_cli()
        self.deploy_script()
        self.deploy_cli()
        return self.cli

    def load_manifest(self) -> dict:
        try:
            return yaml.safe_load(self.manifest_io)
        except yaml.YAMLError as e:
            print("load_manifest", e)
            return {}

    def deploy_cli(self) -> str:
        cli_path = f"{CLIFFY_CLI_DIR}/{self.manifest.name}.py"
        write_to_file(cli_path, self.cli.code)
        return cli_path

    def deploy_script(self) -> str:
        script_path = f"{PYTHON_BIN}/{self.manifest.name}"
        write_to_file(script_path, self.get_cli_script(), executable=True)
        return script_path

    def get_cli_script(self) -> str:
        return f"""#!{PYTHON_EXECUTABLE}
import sys
from cliffy.clis.{self.manifest.name} import cli

if __name__ == '__main__':
    sys.exit(cli())"""


def write_to_file(path, text, executable=False) -> bool:
    try:
        with open(path, "w") as s:
            s.write(text)
    except Exception as e:
        print("write_to_file", e)
        return False

    if executable:
        make_executable(path)

    return True


def make_executable(path) -> None:
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)
