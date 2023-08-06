import typing as t
import types
import types


Writable = t.Union[str, 'Builder', t.Any]


class Builder(list):
    def __init__(self, *bases: str, separator: t.Optional[str] = ' ') -> None:
        self.write(bases)
        self.separator: str = separator

    def build(self):
        return self.separator.join(self)

    def write(self, value: Writable):
        value_type = type(value)

        if value_type == str:
            self.append(value)
        elif issubclass(value_type, Builder):
            self.write(value.build())
        elif value_type in (list, tuple, map, filter, set, types.GeneratorType):
            self.extend(value)
        elif callable(value):
            self.write(value())
        else:
            self.append(str(value))

        return self

    def write_if(self, condition: bool, code: Writable, or_else: t.Optional[Writable] = None):
        if condition:
            self.write(code)
        elif or_else is not None:
            self.write(or_else)
        return self


class SurroundBuilder(Builder):
    def __init__(self, *base: str, surround: t.Optional[t.List[str]] = '""', separator: t.Optional[t.Union[str, t.List]] = '') -> None:
        self.surround = surround
        self.separator = separator
        self.write(base)

    def build(self) -> str:
        return f'{self.surround[0]}{super().build()}{self.surround[1]}'
