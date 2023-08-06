from detacher import detach

__all__ = {"daemon", "detach"}

def daemon(func) -> None:
    """
    Decorator to detach function from Python interpreter
    Spawns a new python interpreter to run function within
    """
    def wrap():
        detach(func)
    return wrap