import json

from .services.folders import FolderService
from .services.sessions import SessionService
from .services.tags import TagService


SERVICES = {
    "folders": FolderService(),
    "sessions": SessionService(),
    "tags": TagService(),
}


def format_response_json(
    message: str,
    status_code: int
) -> str:
    return json.dumps({
        "message": message,
        "status_code": status_code
    })


def handlecmd(request: str):
    data: dict = json.loads(request)

    args = data["args"]
    kwargs = data["kwargs"]
    flags = data["flags"]
    
    service_instance: FolderService = SERVICES.get(args[0])
    if not service_instance:
        return format_response_json(f"Service not found: {args[0]}", 1)
    if not hasattr(service_instance, args[1]):
        return format_response_json(f"Method not found: {args[0]}.{args[1]}", 1)
    method = service_instance.__getattribute__(args[1])

    try:
        response = method(
            args=args[2:],
            flags=flags,
            **kwargs
        )
    except Exception as e:
        if "v" in flags:
            response = f"An error occurred: {e}", 1
        else:
            response = "An error occurred", 1
    finally:
        return format_response_json(*response)
