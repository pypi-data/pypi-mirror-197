"""
Serves as the entry point for runing the SHADY backend.
"""
import shadybackend.log as log
from pathlib import Path
from signal import SIGINT, signal
from sys import exit
from threading import Thread
from typing import Any, Dict

from shadybackend.api_tools import G, HookTypes, call_hooks
from shadybackend.bridges import BRIDGES
from shadybackend.demon import run_api_demon

# Default location for the web tree to be located
DEFAULT_WEB_ROOT = "./tree"
# Default location for the api to be collected from
DEFAULT_API_ROOT = "./api.py"


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
    api_thread = Thread(target=run_api_demon, name="API Demon",
                        args=[root_path, api_path], daemon=True)
    bridge_thread = Thread(
        target=bridge_class.build_bridge,
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
    with open("keys") as f:
        token = f.readline()[:-1]
    run_top_level({"discord_token": token}, "fish")


if __name__ == "__main__":
    run()
