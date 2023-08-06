from inspect import Signature, signature
from typing import Any, Dict, List, Type, TypeVar, _GenericAlias  # type: ignore

from ..dtos import Registration
from ..enums import Scope
from ..helpers import TypeHelpers
from ..interfaces import IScopeManager


class SingletonScopeManager(IScopeManager):
    __resolved_instances: Dict[Type, Any]
    __base_types: List[Type]
    __ignore_parameters: List[str]

    def __init__(self, base_types: List[Type]) -> None:
        self.__resolved_instances = {}
        self.__base_types = base_types
        self.__ignore_parameters = ["self", "args", "kwargs"]

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.SINGLETON

    def is_same_registration_scope(
        self, interface: Type, container: Dict[Type, Registration]
    ) -> bool:
        registration: Registration = container[interface]
        return registration.scope == Scope.SINGLETON

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        error_message: str = ""
        if interface in self.__resolved_instances.keys():
            return self.__resolved_instances[interface]
        else:
            if interface in container.keys():
                implementation: Any = container[interface].implementation
                if type(implementation) in self.__base_types:  # Class Registration
                    if type(implementation) == _GenericAlias:  # type: ignore
                        self.__resolved_instances[interface] = self.resolve_generic(
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
                                    warning_message: str = f"Warning Singleton type: {TypeHelpers.to_string(interface)} registered with Transient dependency: {TypeHelpers.to_string(child_interface)}"
                                    print(warning_message)
                                instance = self.resolve(
                                    interface=child_interface, container=container
                                )
                                kwargs[p] = instance
                        self.__resolved_instances[interface] = implementation(**kwargs)
                elif type(implementation) == type(lambda: ""):
                    self.__resolved_instances[interface] = implementation()
                else:
                    self.__resolved_instances[interface] = implementation
                return self.__resolved_instances[interface]
            else:
                error_message = (
                    f"Cannot resolve type: {TypeHelpers.to_string(interface)}"
                )
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
                    warning_message: str = f"Warning Singleton type: {TypeHelpers.to_string(interface)} registered with Transient dependency: {TypeHelpers.to_string(child_interface)}"
                    print(warning_message)
                instance = self.resolve(interface=child_interface, container=container)
                kwargs[p] = instance
        return implementation(**kwargs)

    @property
    # Exposed for Unit Testing
    def resolved_instances(self) -> Dict[Type, Any]:
        return self.__resolved_instances
