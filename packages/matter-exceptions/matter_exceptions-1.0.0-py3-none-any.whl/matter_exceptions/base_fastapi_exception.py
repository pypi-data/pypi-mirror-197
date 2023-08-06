import json
from typing import Any
from abc import ABC, abstractmethod

from fastapi import HTTPException


class BaseFastAPIException(HTTPException, ABC):
    def __init__(self, description, detail: Any = None):
        self.description = description
        super().__init__(detail=detail, status_code=self.STATUS_CODE)  # type: ignore

    def __init_subclass__(cls, **kwargs):
        for required in ("STATUS_CODE",):
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined")
        return super().__init_subclass__(**kwargs)

    def as_json(self):
        return json.dumps(
            {
                "status_code": self.status_code,
                "description": self.description,
                "detail": self.detail,
            }
        )
