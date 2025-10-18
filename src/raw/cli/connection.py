import socket
import json


def request(args: list, kwargs: dict, flags: list) -> dict:
    
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        client.connect("/tmp/raw.sock")
    except FileNotFoundError:
        return "raw: daemon is not started"

    requestobj = {
        "args": args,
        "kwargs": kwargs,
        "flags": flags,
    }
    
    client.sendall(json.dumps(requestobj).encode())
    response = client.recv(1024).decode()
    if not response:
        return {
            "message": "Daemon did not respond. This may be caused by a critical error", 
            "status_code": 1
        }
    response: dict = json.loads(response)

    return response
