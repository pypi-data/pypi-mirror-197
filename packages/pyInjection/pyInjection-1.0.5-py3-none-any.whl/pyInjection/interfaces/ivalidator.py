from typing import Type, Any
from abc import ABC, abstractmethod

class IValidator(ABC):
    @abstractmethod
    def is_valid(self, interface: Type, implementation: Any) -> bool:
        pass
