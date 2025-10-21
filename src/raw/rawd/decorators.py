from ..config import load_config


CONFIG = load_config()


def provide_conf(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, __cnf=CONFIG)
    
    return wrapper
