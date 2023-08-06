from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from ..dtos import Registration
from ..enums import Scope


class IScopeManager(ABC):
    @abstractmethod
    def can_resolve(self, scope: Scope) -> bool:
        pass

    @abstractmethod
    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        pass
