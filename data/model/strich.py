from __future__ import annotations

import datetime
from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.model.model_base import ModelBase

if TYPE_CHECKING:
    from data.model.genusswand import Genusswand


class Strich(ModelBase):
    __tablename__ = "Striche"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
    timestamp: Mapped[float] = mapped_column(default=None)
    reason: Mapped[str] = mapped_column(default=None)
    mistaker: Mapped[str] = mapped_column(default=None)
    reporter: Mapped[str] = mapped_column(default=None)
    genusswand_uuid: Mapped[str] = mapped_column(
        ForeignKey("Genusswaende.uuid"), init=False, default=None, repr=False
    )
    genusswand: Mapped[Genusswand] = relationship(init=False, default=None)
