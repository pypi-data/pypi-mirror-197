from . import jskiner
from . import schema  # noqa: F401
from .jskiner import InferenceEngine  # noqa: F401

__doc__ = jskiner.__doc__
if hasattr(jskiner, "__all__"):
    __all__ = jskiner.__all__
    __all__.append('schema')
    __all__.append('InferenceEngine')
