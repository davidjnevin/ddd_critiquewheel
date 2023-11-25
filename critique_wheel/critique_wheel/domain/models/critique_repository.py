import abc
from typing import List, Optional

from critique_wheel.critiques.value_objects import CritiqueId
from critique_wheel.domain.models.critique import Critique


class AbstractCritiqueRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, critique: Critique) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, critique_id: CritiqueId) -> Optional[Critique]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Critique]:
        raise NotImplementedError
