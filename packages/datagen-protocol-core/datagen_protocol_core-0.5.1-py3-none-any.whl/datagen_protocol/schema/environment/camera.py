from enum import Enum
from typing import Optional

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.d3 import Point, Rotation
from pydantic import BaseModel, Field


class Projection(str, Enum):
    PERSPECTIVE = "perspective"
    PANORAMIC = "panoramic"
    ORTHOGRAPHIC = "orthographic"


class Wavelength(str, Enum):
    VISIBLE = "visible"
    NIR = "nir"


class IntrinsicParams(BaseModel):
    projection: Projection = fields.enum(Projection, conf["camera"]["projection"])
    wavelength: Wavelength = fields.enum(Wavelength, conf["camera"]["wavelength"])
    resolution_height: int = fields.numeric(conf["camera"]["res"]["height"])
    resolution_width: int = fields.numeric(conf["camera"]["res"]["width"])
    fov_horizontal: int = fields.numeric(conf["camera"]["fov"]["horizontal"])
    fov_vertical: int = fields.numeric(conf["camera"]["fov"]["vertical"])
    sensor_width: float = fields.numeric(conf["camera"]["sensor"]["width"])
    fps: Optional[int] = None

    def dict(self, exclude_none=True, **kwargs):
        return super().dict(exclude_none=exclude_none, **kwargs)


class ExtrinsicParams(BaseModel):
    location: Point = fields.point(conf["camera"]["location"])
    rotation: Rotation = fields.rotation(conf["camera"]["rotation"])


class Camera(BaseModel):
    name: str = conf["camera"]["name"]
    extrinsic_params: ExtrinsicParams = Field(default_factory=ExtrinsicParams)
    intrinsic_params: IntrinsicParams = Field(default_factory=IntrinsicParams)

    @property
    def extrinsics(self) -> ExtrinsicParams:
        return self.extrinsic_params

    @extrinsics.setter
    def extrinsics(self, extrinsic_params: ExtrinsicParams) -> None:
        self.extrinsic_params = extrinsic_params

    @property
    def intrinsics(self) -> IntrinsicParams:
        return self.intrinsic_params

    @intrinsics.setter
    def intrinsics(self, intrinsic_params: IntrinsicParams) -> None:
        self.intrinsic_params = intrinsic_params
