import os
import sys
import typer

from endoscopie import controller
from endoscopie import utils
from endoscopie.logarithm import Logarithm
from pathlib import Path
from rich import print
from typing import Optional

__version__ = '0.1.1'

app = typer.Typer()

global yam

logger = Logarithm(__name__)


@app.command()
def run(target: Optional[Path] = typer.Option(..., "--config",
                                              help="Set YAML file in which the datas required for image verify.")):
    _init(__version__)
    message = "Initializing the Endoscopie..."
    logger.info(message)

    _check(target)
    _setenv(yam.get('openstack'))
    _provision(target)


@app.command()
def cleanup():
    destroy: bool = typer.confirm("Are you sure you want to delete server(s)?", abort=True)
    _init(__version__)
    _clean_up(destroy)


def _clean_up(destroy: bool):
    message = "Start cleaning up the resources you used for testing."
    logger.info(message)

    try:
        controller.cleanup(destroy)
        utils.unset_variables()
    except Exception as e:
        logger.error(f"Failed to delete server that were used for the test. - {e}")

    logger.info("Finished cleaning.")
    sys.exit(0)


def _init(version: str) -> None:
    os.system('clear')
    print(utils.description(version))

    return None


def _check(target: Optional[Path]):
    logger.debug("Loading configurations...")

    if not _validation(target):
        message = "Failed to load configuration file. Please check the YAML file."
        print(f"[red]{message}[/red]")
        logger.error(message)

        sys.exit(1)

    logger.debug("Configuration successfully loaded.")


def _validation(target: Optional[Path]) -> bool:
    is_valid = False

    if _exist_file(target):
        if _is_malformed(target):
            is_valid = True

    return is_valid


def _exist_file(target: Optional[Path]) -> bool:
    output, error = utils.check_file_exist(target)

    if error is not None:
        logger.error(error)
        return False

    return True


def _is_malformed(target: Optional[Path]) -> bool:
    global yam
    yam = utils.load_yaml_file(target)

    if not yam:
        logger.error("Invalid YAML file (empty)")
        return False

    if 'openstack' not in yam.keys():
        logger.error("Invalid YAML file (Openstack Credential information is missing)")
        print("No Openstack Credential Information.")
        return False

    return True


def _setenv(openstack: dict) -> None:
    utils.setenv(openstack)


def _provision(target: Optional[Path]) -> None:
    servers = controller.provision(target)
    controller.verify(servers)



def main() -> int:

    app()
    return 0


if __name__ == "__main__":
    sys.exit(main())