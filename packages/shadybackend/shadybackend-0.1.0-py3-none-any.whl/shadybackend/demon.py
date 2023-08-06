"""
This is the default API demon that is used for the shadybackend.
"""
from collections import deque
import logging as log
from pathlib import Path
from time import sleep
from typing import List

from shadybackend.api_tools import (
    G,
    HOOKS,
    HookTypes,
    call_hooks,
    collect_apis,
    process_request,
)

G["Q"] = deque()

MAX_SLEEP = 1


def run_api_demon(root: Path, api_paths: List[Path]) -> None:
    """
    Run the app, with self restarting on recoverable errors.

    :args root: The root of the web tree.
    :args api_paths: The paths where API definitions are found.
    """
    G["root"] = root
    G["run"] = True
    call_hooks(HookTypes.INIT)
    for path in api_paths:
        collect_apis(path)
    try:
        while (G["run"]):
            if (len(G["Q"])):
                call_hooks(HookTypes.PRE)
                req = G["Q"].pop()
                G["req"] = req
                try:
                    process_request(req)
                except Exception as e:
                    call_hooks(HookTypes.ERR)
                    err = e
                    log.error(f"Failed to process {req}: {e}")
                else:
                    call_hooks(HookTypes.OK)
                finally:
                    call_hooks(HookTypes.POST)
            else:
                call_hooks(HookTypes.WAIT)
                sleep(MAX_SLEEP)
        call_hooks(HookTypes.EXIT)
    except Exception as e:
        log.fatal(f"Fatal err: {e}")
        call_hooks(HookTypes.FATAL)


log.debug("Loaded demon lib.")
