from enum import Enum
from typing import Callable
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

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
        with open(settings.MEDIA_ROOT / image.name, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
            return "http://localhost:8000" + settings.MEDIA_URL + image.name
    else:
        return None