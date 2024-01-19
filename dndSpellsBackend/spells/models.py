from email.mime import image
from email.policy import default
from enum import Enum
from django.conf import settings
from django.forms import ChoiceField
from mongoengine import *
from django.core.files.uploadedfile import UploadedFile

class CastType(Enum):
    Action = "Action"
    Bonus = "Bonus"
    Reaction = "Reaction"
    Time = "Time"
    Unknown = "Unknown"
    
    def __str__(self):
        return self.value

class SpellRangeType(Enum):
    Self = "Self"
    Touch = "Touch"
    Sight = "Sight"
    Special = "Special"
    Unlimited = "Unlimited"
    Units = "Units"
    Unknown = "Unknown"
    
    def __str__(self):
        return self.value

class SpellSchool(Enum):
    abjuration = "abjuration"
    conjuration = "conjuration"
    divination = "divination"
    enchantment = "enchantment"
    evocation = "evocation"
    illusion = "illusion"
    necromancy = "necromancy"
    transmutation = "transmutation"
    unknown = "unknown"
    
    def __str__(self):
        return self.value

class ComponentType(Enum):
    Verbal = "Verbal"
    Somatic = "Somatic"
    Material = "Material"
    
    def __str__(self):
        return self.value


class ClassType(Enum):
    Artificer = "artificer"
    Bard = "bard"
    Cleric = "cleric"
    Druid = "druid"
    Paladin = "paladin"
    Ranger = "ranger"
    Sorcerer = "sorcerer"
    Warlock = "warlock"
    Wizard = "wizard"
    
    def __str__(self):
        return self.value

class Spells(Document):
    _id = ObjectIdField()
    name = StringField()
    description = StringField()
    level = IntField()
    school = EnumField(SpellSchool, default=SpellSchool.unknown)
    duration = StringField()
    is_concentration = BooleanField()
    cast_type = EnumField(CastType, default=CastType.Unknown)
    cast_time = IntField()
    is_ritual = BooleanField()
    range_type = EnumField(SpellRangeType, default=SpellRangeType.Unknown)
    spell_range = StringField()
    has_upcast = BooleanField()
    upcast = StringField()
    components = ListField(EnumField(ComponentType))
    component_material = StringField()
    classes = ListField(EnumField(ClassType))
    image_url = URLField()
    is_recommended = BooleanField(default=False)
    url = URLField()
    
    meta = {
        'indexes': [
            'classes',
            'level',
        ]
    }
    
    def save(self, *args, **kwargs):
        self.image_url = save_image(self.image_url)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = "spells"

class SpellClasses(Document):
    _id = ObjectIdField()
    name = StringField(unique = True)
    image_url = URLField()
    
    def save(self, *args, **kwargs):
        self.image_url = save_image(self.image_url)
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table = "spell_classes"


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
    
                
    
