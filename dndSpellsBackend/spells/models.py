from email.mime import image
from email.policy import default
from enum import Enum
from django.conf import settings
from django.forms import ChoiceField
from mongoengine import *
from .utils import SpellSchool, CastType, SpellRangeType, ComponentType, ClassType, save_image

class Spells(Document):
    # _id = ObjectIdField()
    name = StringField()
    description = StringField()
    level = IntField()
    school = EnumField(SpellSchool, default=SpellSchool.Unknown)
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
    image_url = StringField(required=False)
    is_recommended = BooleanField(default=False)
    url = URLField(required=False, null=True)
    
    meta = {
        'indexes': [
            'classes',
            'level',
        ],
        # 'id_field': '_id'
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

    
                
    
