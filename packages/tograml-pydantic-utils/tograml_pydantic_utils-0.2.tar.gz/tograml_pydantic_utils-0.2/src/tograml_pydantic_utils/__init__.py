try:
    from .pydantic import TogramlModel
except ImportError:
    from ._logger import logger

    logger.info(
        "Pydantic not installed, to make type hints work for you - install it: "
        "pip install pydantic or "
        "pip install tograml-pydantic-utils[pydantic]"
    )

    __pydantic_all__ = []

else:
    __pydantic_all__ = ["TogramlModel"]

from .mixins import ExcludesNone
from .update_forward_refs_helper import update_forward_refs_helper

__version__ = "0.2"
__all__ = (
    "ExcludesNone",
    "update_forward_refs_helper",
    *__pydantic_all__,
)
