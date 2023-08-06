from enum import Enum
from typing import Optional
from pydantic.fields import Field

from datagen_protocol.schema.attributes import Gender, AccessoryPosition, GlassesStyle, MaskStyle
from datagen_protocol.schema.base import Asset, AttributesList, AssetAttributes, SchemaBaseModel
from datagen_protocol.config import conf
from datagen_protocol.schema import fields


class AccessoryAttributes(AssetAttributes):
    gender: AttributesList[Gender]
    supported_position: AttributesList[AccessoryPosition]


class GlassesAttributes(AccessoryAttributes):
    style: GlassesStyle


class LensColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class FrameColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    GRAY = "gray"
    SILVER = "silver"
    GOLD = "gold"


class GlassesPosition(str, Enum):
    ON_NOSE = "on_nose"


class Glasses(Asset[GlassesAttributes]):
    lens_color: LensColor = fields.enum(LensColor, conf["accessories"]["glasses"]["lens"]["color"])
    lens_reflectivity: float = fields.numeric(conf["accessories"]["glasses"]["lens"]["reflectivity"])
    lens_transparency: float = fields.numeric(conf["accessories"]["glasses"]["lens"]["transparency"])
    frame_color: FrameColor = fields.enum(FrameColor, conf["accessories"]["glasses"]["frame"]["color"])
    frame_metalness: float = fields.numeric(conf["accessories"]["glasses"]["frame"]["metalness"])
    position: GlassesPosition = fields.enum(GlassesPosition, conf["accessories"]["glasses"]["position"])


class MaskColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"
    RED = "red"


class MaskAttributes(AccessoryAttributes):
    style: MaskStyle


class MaskPosition(str, Enum):
    ON_NOSE = "on_nose"
    ON_MOUTH = "on_mouth"
    ON_CHIN = "on_chin"


class MaskTexture(str, Enum):
    CLOTH = "cloth"
    DIAMOND_PATTERN = "diamond_pattern"
    WOVEN = "woven"


class Mask(Asset[MaskAttributes]):
    color: MaskColor = fields.enum(MaskColor, conf["accessories"]["mask"]["color"])
    texture: MaskTexture = fields.enum(MaskTexture, conf["accessories"]["mask"]["texture"])
    position: MaskPosition = fields.enum(MaskPosition, conf["accessories"]["mask"]["position"])
    roughness: float = fields.numeric(conf["accessories"]["mask"]["roughness"])


class Accessories(SchemaBaseModel):
    glasses: Optional[Glasses]
    mask: Optional[Mask]
