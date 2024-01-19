from os import read
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import serializers

from .models import SpellClasses, Spells
from django.conf import settings

class MongoSerializer(serializers.Serializer):
        
    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data) # type: ignore
    
    def update(self, instance, validated_data):
        for name in self.fields:
            if name in validated_data:
                setattr(instance, name, validated_data[name])
        instance.save()
        return instance

    class Meta:
        pass



class ObjectIdField(serializers.Field):
    """ Serializer field for Djongo ObjectID fields """
    def to_internal_value(self, data):
        # Serialized value -> Database value
        return data.to_python()  # Get the ID, then build an ObjectID instance using it

    def to_representation(self, value):
        # Database value -> Serialized value
        if not ObjectId.is_valid(value):  # User submitted ID's might not be properly structured
            raise InvalidId
        return str(value)

# can't use __all__ because of django_mongoengine_filter
class SpellSerializer(MongoSerializer):
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    school = serializers.CharField(read_only=True)
    duration = serializers.CharField(read_only=True)
    is_concentration = serializers.BooleanField(read_only=True)
    cast_type = serializers.CharField(read_only=True)
    cast_time = serializers.IntegerField(read_only=True)
    is_ritual = serializers.BooleanField(read_only=True)
    range_type = serializers.CharField(read_only=True)
    spell_range = serializers.CharField(read_only=True)
    has_upcast = serializers.BooleanField(read_only=True)
    upcast = serializers.CharField(read_only=True)
    components = serializers.ListField(child = serializers.CharField(read_only=True), read_only=True)
    component_material = serializers.CharField(read_only=True)
    classes = serializers.ListField(child = serializers.CharField(read_only=True), read_only=True)
    is_recommended = serializers.BooleanField()
    image_url = serializers.URLField()
    url = serializers.URLField(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST', 'PUT', 'PATCH']:
                self.fields['image_url'] = serializers.FileField(required=False)
        except KeyError:
            pass

    class Meta:
        model = Spells

class SpellClassSerializer(MongoSerializer):
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(read_only=True)
    image_url = serializers.URLField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            if self.context['request'].method in ['POST', 'PUT', 'PATCH']:
                self.fields['image_url'] = serializers.FileField(required=False)
        except KeyError:
            pass
    
    class Meta:
        model = SpellClasses


