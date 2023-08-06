from typing import Type, List

class TypeHelpers:

    @staticmethod
    def to_string(input_type: Type) -> str:
        type_string: str = str(input_type)
        type_split: List[str] = type_string.split('.')
        return f'[{type_split[-1][:-2]}]'
