from typing import Any
from abc import ABC, abstractmethod


class DetailedException(Exception, ABC):
    def __init__(self, description: str, detail: Any = None):
        self.description = description if self.TOPIC in description else f"{self.TOPIC}: {description}"  # type: ignore
        self.detail = detail
        self.type = self.TOPIC.replace(" ", "_").lower()  # type: ignore

    def __init_subclass__(cls, **kwargs):
        for required in ("TOPIC",):
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        return super().__init_subclass__(**kwargs)

    def __reduce__(self):
        return self.__class__, (
            self.description,
            self.detail,
        )

    def __eq__(self, other):
        return other.__reduce__() == self.__reduce__()
