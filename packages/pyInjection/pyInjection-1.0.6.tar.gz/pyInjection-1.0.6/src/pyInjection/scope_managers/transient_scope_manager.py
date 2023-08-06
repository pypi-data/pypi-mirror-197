from inspect import Signature, signature
from typing import Any, Dict, List, Type, TypeVar, _GenericAlias  # type: ignore

from ..dtos import Registration
from ..enums import Scope
from ..helpers import TypeHelpers
from ..interfaces import IScopeManager


class TransientScopeManager(IScopeManager):
    __base_types: List[Type]
    __ignore_parameters: List[str]

    def __init__(self, base_types: List[Type]) -> None:
        self.__base_types = base_types
        self.__ignore_parameters = ["self", "args", "kwargs"]

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.TRANSIENT

    def is_same_registration_scope(
        self, interface: Type, container: Dict[Type, Registration]
    ) -> bool:
        registration: Registration = container[interface]
        return registration.scope == Scope.TRANSIENT

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        error_message: str = ""
        if interface in container.keys():
            implementation: Any = container[interface].implementation
            if type(implementation) in self.__base_types:
                if type(implementation) == _GenericAlias:  # type: ignore
                    return self.resolve_generic(
                        interface=interface, container=container
                    )
                else:
                    kwargs: Any = {}
                    sig: Signature = signature(implementation)
                    for p in sig.parameters:
                        if p not in self.__ignore_parameters:
                            child_interface: Type = sig.parameters[p].annotation
                            if not self.is_same_registration_scope(
                                interface=child_interface, container=container
                            ):
                                error_message = f"Error Transient type: {TypeHelpers.to_string(interface)} registered with Singleton dependency: {TypeHelpers.to_string(child_interface)}"
                                raise Exception(error_message)
                            instance = self.resolve(
                                interface=child_interface, container=container
                            )
                            kwargs[p] = instance
                    return implementation(**kwargs)
            elif type(implementation) == type(lambda: ""):
                return implementation()
            else:
                return implementation
        else:
            error_message = f"Cannot resolve type: {TypeHelpers.to_string(interface)}"
            raise Exception(error_message)

    def resolve_generic(
        self, interface: Type, container: Dict[Type, Registration]
    ) -> Any:
        implementation: Any = container[interface].implementation
        implementation_type: Type = implementation.__origin__
        generic_class: Type = implementation.__args__[0]
        kwargs: Any = {}
        sig: Signature = signature(implementation_type)
        for p in sig.parameters:
            if p not in self.__ignore_parameters:
                child_interface: Type = sig.parameters[p].annotation
                if type(child_interface) == _GenericAlias:  # type: ignore
                    child_interface_generic_type = child_interface.__args__[0]
                    if type(child_interface_generic_type) == TypeVar:
                        ## Generic type needs to be passed down from parent
                        child_interface.__args__ = (generic_class,)
                if not self.is_same_registration_scope(
                    interface=child_interface, container=container
                ):
                    error_message = f"Error Transient type: {TypeHelpers.to_string(interface)} registered with Singleton dependency: {TypeHelpers.to_string(child_interface)}"
                    raise Exception(error_message)
                instance = self.resolve(interface=child_interface, container=container)
                kwargs[p] = instance
        return implementation(**kwargs)
