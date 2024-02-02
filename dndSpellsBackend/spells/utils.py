from enum import Enum
import random
from typing import Callable
import uuid
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from dndSpellsBackend.storage_backends import PublicMediaStorage

class EnumPrint(Enum):
    def __repr__(self):
        return self.value
    
    def __str__(self):
        return self.value

class CastType(EnumPrint):
    Action = "Action"
    Bonus = "Bonus"
    Reaction = "Reaction"
    Time = "Time"
    Unknown = "Unknown"

class SpellRangeType(EnumPrint):
    Self = "Self"
    Touch = "Touch"
    Sight = "Sight"
    Special = "Special"
    Unlimited = "Unlimited"
    Units = "Units"
    Unknown = "Unknown"

class SpellSchool(EnumPrint):
    Abjuration = "abjuration"
    Conjuration = "conjuration"
    Divination = "divination"
    Enchantment = "enchantment"
    Evocation = "evocation"
    Illusion = "illusion"
    Necromancy = "necromancy"
    Transmutation = "transmutation"
    Unknown = "unknown"

class ComponentType(EnumPrint):
    Verbal = "Verbal"
    Somatic = "Somatic"
    Material = "Material"


class ClassType(EnumPrint):
    Artificer = "artificer"
    Bard = "bard"
    Cleric = "cleric"
    Druid = "druid"
    Paladin = "paladin"
    Ranger = "ranger"
    Sorcerer = "sorcerer"
    Warlock = "warlock"
    Wizard = "wizard"

def validate_comma_separated_list(value: str, field_type: type, sanitizer: Callable[[str], str] = lambda x: x.strip()) -> list:
    split_v = value.strip("[] ").split(",")
    return_list = [None for _ in split_v]
    for i, v in enumerate(split_v):
        return_list[i] = (field_type(sanitizer(v)))
    return return_list

def save_image(image):
    if type(image) == str:
        return image
    if hasattr(image, 'url'):
        return image.url
    if isinstance(image, UploadedFile):
        image.name = f"{get_random_hash()}"
        upload = PublicMediaStorage()
        file_name = upload.save(image.name, image)
        return file_name
    else:
        return None

def get_random_hash():
    return uuid.uuid4().hex