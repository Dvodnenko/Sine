from .icm import INTERNAL_CMD_MAP
from .connection import request
from ...common import drill, ARG_RE


def resolve_callback(args):
    """
    Find and return the callback that actually 
    runs the logic user is asking for

    If the callback is internal - return the 
    callback object itself; if its external - 
    prepare everything for request
    """

    callback = drill(
        INTERNAL_CMD_MAP,
        args, ARG_RE, conditions=[callable]
    )
    if callback:
        return callback, True
    return request, False
