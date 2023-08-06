from typing import Type, Any, Dict
from abc import ABC, abstractmethod
from ..enums import Scope
from ..dtos import Registration

class IScopeManager(ABC):
    @abstractmethod
    def can_resolve(self, scope: Scope) -> bool:
        pass

    @abstractmethod
    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        pass
