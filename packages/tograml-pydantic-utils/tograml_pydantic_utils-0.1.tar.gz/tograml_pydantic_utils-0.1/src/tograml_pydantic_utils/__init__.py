try:
    import pydantic
except ImportError:
    from ._logger import logger

    logger.info(
        "Pydantic not installed, to make type hints work for you - install it: "
        "pip install pydantic or "
        "pip install tograml-pydantic-utils[pydantic]"
    )

from .mixins import ExcludesNone
from .update_forward_refs_helper import update_forward_refs_helper

__version__ = "0.1"
__all__ = (
    "ExcludesNone",
    "update_forward_refs_helper",
)
