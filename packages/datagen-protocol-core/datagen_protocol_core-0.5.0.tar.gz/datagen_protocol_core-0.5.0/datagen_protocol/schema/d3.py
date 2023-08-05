import abc
from typing import TypeVar, Type

from pydantic import Field

from datagen_protocol.config import conf
from datagen_protocol.schema.base import SchemaBaseModel


class Coords3D(SchemaBaseModel):
    x: float = Field(ge=conf["d3"]["boundaries"]["min"], le=conf["d3"]["boundaries"]["max"])
    y: float = Field(ge=conf["d3"]["boundaries"]["min"], le=conf["d3"]["boundaries"]["max"])
    z: float = Field(ge=conf["d3"]["boundaries"]["min"], le=conf["d3"]["boundaries"]["max"])


class Point(Coords3D):
    pass


class Vector(Coords3D):
    pass


class Rotation(SchemaBaseModel):
    yaw: float
    roll: float
    pitch: float
