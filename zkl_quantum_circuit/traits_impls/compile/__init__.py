import importlib

from .flatten import FlattenPass
from .freeze import FreezePass

importlib.import_module(".impls", __package__)
del importlib
