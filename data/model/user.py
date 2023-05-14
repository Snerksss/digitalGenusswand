from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.model.model_base import ModelBase
from data.model.genusswand import Genusswand


if TYPE_CHECKING:
    pass


class User(ModelBase):
    __tablename__ = "Users"

    username: Mapped[str] = mapped_column(default=None, primary_key=True)
    first_name: Mapped[str] = mapped_column(default=None)
    last_name: Mapped[str] = mapped_column(default=None)
    email: Mapped[str] = mapped_column(default=None, unique=True)
    passwd: Mapped[str] = mapped_column(default=None)
    genusswaende: List[Genusswand] = field(init=False, default_factory=list)
    _genusswaende: Mapped[List[Genusswand]] = relationship(
        init=False, default_factory=list, repr=False, back_populates="user"
    )

    @property
    def genusswaende(self) -> list[genusswaende]:
        return self._genusswaende

    @genusswaende.setter
    def genusswaende(self, genusswaende: list[Genusswand]):
        if isinstance(genusswaende, list):
            for genusswand in genusswaende:
                genusswand.user = self
            self._genusswaende = genusswaende
        else:
            self._genusswaende = []
