"""
Serves as the entry point for runing the SHADY backend.
"""
from json import loads
from pathlib import Path
from signal import SIGINT, signal
from sys import exit
from threading import Thread
from typing import Any, Dict

from shadybackend.log import log
from shadybackend.api_tools import G, HookTypes, call_hooks
from shadybackend.bridges import BRIDGES
from shadybackend.demon import run_api_demon
from argparse import ArgumentParser

# Default location for the web tree to be located
DEFAULT_WEB_ROOT = "./tree"
# Default location for the api to be collected from
DEFAULT_API_ROOT = "./api.py"
# Shady backend version.
VERSION = 1


def run_top_level(start_g: Dict[str, Any], bridge: str,
                  root: str = DEFAULT_WEB_ROOT,
                  api: str = DEFAULT_API_ROOT) -> None:
    """
    Starts the provided hook bridge and runs the default demon.

    :args start_g: JSON string that will be loaded as the default global
    dictionary.
    :args bridge: The bridge app to use. See the bridge module for options.
    :args root: The path as a string to the root of the web tree.
    :args api: The path as a string to the api to be run.
    """
    root_path = Path(root)
    api_path = [Path(api)]
    log.debug(f"Using {root_path=} {api_path=}")
    G.update(start_g)
    log.debug(f"Using {start_g=}")
    bridge_class = BRIDGES.get(bridge, None)
    if (bridge_class is None):
        log.fatal(f"Bridge '{bridge}' not found.")
        exit(1)
    bridge_object = bridge_class()
    api_thread = Thread(target=run_api_demon, name="API Demon",
                        args=[root_path, api_path], daemon=True)
    bridge_thread = Thread(
        target=bridge_object.build_bridge,
        name="Hook Bridge",
        args=[G],
        daemon=True)
    log.info("Starting API Demon thread")
    api_thread.start()
    log.info("Starting API Bridge thread")
    bridge_thread.start()
    while True:
        ...


def on_exit(signum, stack) -> None:
    """
    Calls the redigested EXIT hooks on kill signal
    """
    log.fatal("Killed by user")
    call_hooks(HookTypes.EXIT)
    exit(0)


signal(SIGINT, on_exit)


def run() -> None:
    """
    Runs the CLI parser and then starts the top level.
    """
    parser = ArgumentParser(
        prog='Shady Backend',
        description=('CLI interface to run parts of'
                     ' the shadybackend through DAD.'),
        epilog=f'Using: Shady Backend Release {VERSION}')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Be chatty.")
    parser.add_argument("--tree", default=DEFAULT_WEB_ROOT,
                        help="Provide the location of the web root.")
    parser.add_argument("--api", default=DEFAULT_API_ROOT,
                        help="Provide the location of the api.py file.")
    parser.add_argument("bridge", metavar='BRIDGE', choices=BRIDGES.keys(),
                        help="The name of the bridge to use.")
    parser.add_argument("start_g", metavar='G',
                        help="A JSON dict to initialize G to.")
    args = parser.parse_args()
    if (args.verbose):
        log.basicConfig(level=log.DEBUG)
    else:
        log.basicConfig(level=log.INFO)
    G = loads(args.start_g)
    run_top_level(G, args.bridge, args.tree, args.api)


if __name__ == "__main__":
    run()
