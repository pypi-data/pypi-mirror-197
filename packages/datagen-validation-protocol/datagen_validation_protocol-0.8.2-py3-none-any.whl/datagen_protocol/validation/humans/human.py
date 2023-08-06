from typing import List

from pydantic import validator

from datagen_protocol.schema.humans import Human, Accessories
from datagen_protocol.schema.environment import Camera, Light, Background, Wavelength
from datagen_protocol.schema import humans as humans_core_schema


class HumanDatapoint(humans_core_schema.HumanDatapoint):
    @validator("lights", always=True)
    def lights_and_not_nir_mutually_exclusive(cls, lights, values) -> List[Light]:
        has_lights = lights is not None and len(lights) > 0
        if has_lights and not cls._is_set_to_nir(values["camera"]):
            raise ValueError("Lights are only relevant if the camera is using 'nir' wavelength")
        return lights

    @validator("background", always=True)
    def background_and_nir_mutually_exclusive(cls, background, values) -> Background:
        if background is not None and cls._is_set_to_nir(values["camera"]):
            raise ValueError("Background is only relevant if the camera is not using 'nir' wavelength")
        return background

    @staticmethod
    def _is_set_to_nir(camera: Camera) -> bool:
        return camera.intrinsics.wavelength == Wavelength.NIR

    @validator("accessories", always=True)
    def mask_and_facial_hair_mutually_exclusive(cls, accessories, values: dict) -> Accessories:
        if accessories and accessories.mask and cls._has_facial_hair(values["human"]):
            raise ValueError("Facial hair and masks are mutually exclusive")
        return accessories

    @staticmethod
    def _has_facial_hair(human: Human) -> bool:
        return bool(human.head.facial_hair)
