# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class Work(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Work - a model defined in OpenAPI

        unique: The unique of this Work.
        info: The info of this Work [Optional].
    """

    unique: Dict[str, Any]
    info: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

Work.update_forward_refs()
