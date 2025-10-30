from typing import Any, Generator

from ..icmds.general import raw_init
from ..icmds.daemon import daemon_start, daemon_stop


INTERNAL_CMD_MAP = {
    "init": raw_init,
    "daemon": {
        "start": daemon_start,
        "stop": daemon_stop,
    },
}


def drill(
    branch: dict,
    args: list[str],
    ci: int = 0
):
    next_: Generator[Any, Any, Any] | dict = branch.get(args[ci]) # callback itself or next branch
    if not callable(next_): # then it is not the destination, keep drilling
        return drill(next_, args, ci+1)
    return next_
