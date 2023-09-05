__version__ = "0.0.1"

import logging
_LOGGER = logging.getLogger("aiofastgate")
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())



from .api import FastGateApi, FastGateDevice
from .exceptions import LoginFailed, InvalidCredentials, FastGateException

__all__ = ["FastGateApi", "FastGateDevice"]
