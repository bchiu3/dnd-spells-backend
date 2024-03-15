from enum import Enum
import random
from typing import Any, Callable, Optional
import uuid
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from dndSpellsBackend.storage_backends import PublicMediaStorage

class EnumPrint(Enum):
    """Enum class with __str__ and __repr__ methods"""
    
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
    """
    Validate a comma-separated list of values and return a list of the specified type after applying the provided sanitizer function to each value.

    Key Arguments:
        value (str): The comma-separated list of values.
        field_type (type): The type to which each value should be converted.
        sanitizer (Callable[[str], str], optional): The function used to sanitize each value. Defaults to lambda x: x.strip().

    Returns:
        list: A list of values of the specified type after applying the sanitizer function.
    """
    split_v = value.strip("[] ").split(",")
    return_list = [None for _ in split_v]
    for i, v in enumerate(split_v):
        return_list[i] = (field_type(sanitizer(v)))
    return return_list

def save_image(image: Any) -> Optional[str]:
    """
    Save the given image based on its type and return the appropriate image URL or file name.

    Key Arguments:
    image (Any): The image object to be saved.

    Returns:
    str|None: The URL of the image if it's a URL or an UploadedFile, or None if the image type is not recognized.
    """
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

def get_random_hash() -> str:
    """
    Generate a random hash value and return it as a string.

    Returns:
        str: A randomly generated hexadecimal hash string.
    """
    return uuid.uuid4().hex