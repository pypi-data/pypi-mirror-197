from __future__ import annotations

import signal
import sys


__all__ = [
    "register",
    "deregister",
]


def _noop(*_, **__):
    pass


class __SigtermHandler:
    """
    Simple wrapper that bundles functions to register and deregister
    functions to be called on receiving SIGTERM.
    """
    funcs = {}
    previous = _noop

    @classmethod
    def register(cls, key, func):
        cls.funcs[key] = func

    @classmethod
    def deregister(cls, key):
        cls.funcs.pop(key, None)

    @classmethod
    def terminate(cls, sig, frame):
        for f in cls.funcs.values():
            f()
        cls.previous(sig, frame)
        print("Terminated")
        sys.exit(143)

    @classmethod
    def enable(cls):
        cls.previous = signal.signal(signal.SIGTERM, cls.terminate)


register = __SigtermHandler.register
deregister = __SigtermHandler.deregister


def enable():
    signal.signal(signal.SIGTERM, __SigtermHandler.terminate)
