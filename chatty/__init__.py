'''Chat Bot Stuff'''

from .connection import Connection


def create(*args, **kwargs):
    """Helper function for the creation of connections."""
    return Connection(*args, **kwargs)
