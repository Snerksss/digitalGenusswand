from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.model.model_base import ModelBase
from data.model.strich import Strich

if TYPE_CHECKING:
    from data.model.user import User


class Genusswand(ModelBase):
    __tablename__ = "Genusswaende"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
    name: Mapped[str] = mapped_column(default=None)
    user_username: Mapped[str] = mapped_column(
        ForeignKey("Users.username"), init=False, default=None, repr=False
    )
    user: Mapped[User] = relationship(init=False, default=None)
    striche: List[Strich] = field(init=False, default_factory=list)
    _striche: Mapped[List[Strich]] = relationship(
        init=False, default_factory=list, repr=False, back_populates="genusswand"
    )

    @property
    def striche(self) -> list[striche]:
        return self._striche

    @striche.setter
    def striche(self, striche: list[Strich]):
        if isinstance(striche, list):
            for strich in striche:
                strich.genusswand = self
            self._striche = striche
        else:
            self._striche = []

