import pydantic

from .mixins import ExcludesNone


class TogramlModel(ExcludesNone, pydantic.BaseModel):  # pragma: no cover
    """
    A base model that`s excludes :class:`None`
    """
