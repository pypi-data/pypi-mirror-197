import json
from typing import Any
from abc import ABC, abstractmethod

from http.client import HTTPException


class BaseAPIException(HTTPException, ABC):
    def __init__(self, description, detail: Any = None):
        self.description = description
        self.detail = detail
        super().__init__()

    def __init_subclass__(cls, **kwargs):
        for required in ("STATUS_CODE",):
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        return super().__init_subclass__(**kwargs)

    def as_json(self):
        return json.dumps(
            {
                "status_code": self.STATUS_CODE,  # type: ignore
                "description": self.description,
                "detail": self.detail,
            }
        )
