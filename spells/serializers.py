from email.policy import default
from os import read
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import serializers

from dndSpellsBackend.storage_backends import PublicMediaStorage
from .utils import hasS3, validate_comma_separated_list, CastType, ClassType, ComponentType, SpellRangeType, SpellSchool
from .models import Spells, SpellClasses, Feats
from django.conf import settings


class MongoSerializer(serializers.Serializer):

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)  # type: ignore

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
        # User submitted ID's might not be properly structured
        if not ObjectId.is_valid(value):
            raise InvalidId
        return str(value)

# can't use __all__ because of django_mongoengine_filter


class SpellSerializer(MongoSerializer):
    """Serializer for spells"""
    name = serializers.CharField()
    description = serializers.CharField()
    level = serializers.IntegerField()
    school = serializers.ChoiceField(
        choices=[(member.value, member.name) for member in SpellSchool])
    duration = serializers.CharField()
    is_concentration = serializers.BooleanField()
    cast_type = serializers.ChoiceField(
        choices=[(member.value, member.name) for member in CastType])
    cast_time = serializers.IntegerField(default=0)
    is_ritual = serializers.BooleanField()
    range_type = serializers.ChoiceField(
        choices=[(member.value, member.name) for member in SpellRangeType])
    spell_range = serializers.CharField()
    has_upcast = serializers.BooleanField()
    upcast = serializers.CharField(default="")
    components = serializers.ListField(child=serializers.ChoiceField(
        choices=[(member.value, member.name) for member in ComponentType]))
    component_material = serializers.CharField(default="")
    classes = serializers.ListField(child=serializers.ChoiceField(
        choices=[(member.value, member.name) for member in ClassType]))
    is_recommended = serializers.BooleanField()
    image_url = serializers.SerializerMethodField()
    url = serializers.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST', 'PUT', 'PATCH']:
                self.fields['image_url'] = serializers.FileField(
                    required=False)
                self.fields['components'] = serializers.CharField(default="")
                self.fields['classes'] = serializers.CharField(default="")
                if not hasS3():
                    self.fields['image_url'] = serializers.CharField(
                        required=False)
        except KeyError:
            pass

    def get_image_url(self, obj):
        if obj.image_url:
            if hasS3():
                return PublicMediaStorage().url(obj.image_url)
            return obj.image_url
        return None

    def validate(self, data):
        if data['level'] < 0:
            raise serializers.ValidationError("Level must be greater than 0")
        if data['components']:
            try:
                data['components'] = validate_comma_separated_list(
                    data['components'], ComponentType, lambda x: x.strip().title())
            except:
                raise serializers.ValidationError("Invalid component type")
        if data['classes']:
            try:
                data['classes'] = validate_comma_separated_list(
                    data['classes'], ClassType, lambda x: x.strip().lower())
            except:
                raise serializers.ValidationError("Invalid class type")
        return data

    class Meta:
        model = Spells


class FeatsSerializer(MongoSerializer):
    """Serializer for feats"""
    name = serializers.CharField()
    description = serializers.CharField()
    prerequisite = serializers.CharField(default="")
    image_url = serializers.URLField(required=False)
    url = serializers.URLField(required=False)
    has_prerequisite = serializers.BooleanField()
    is_recommended = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST', 'PUT', 'PATCH']:
                self.fields['image_url'] = serializers.FileField(
                    required=False)
                if not hasS3():
                    self.fields['image_url'] = serializers.CharField(
                        required=False)
        except KeyError:
            pass

    def get_image_url(self, obj):
        if obj.image_url:
            if hasS3():
                return PublicMediaStorage().url(obj.image_url)
            return obj.image_url
        return None

    class Meta:
        model = Feats


class SpellClassSerializer(MongoSerializer):
    """Serializer for dnd classes"""
    _id = ObjectIdField(read_only=True)
    name = serializers.CharField(read_only=True)
    image_url = serializers.URLField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            if self.context['request'].method in ['POST', 'PUT', 'PATCH']:
                self.fields['image_url'] = serializers.FileField(
                    required=False)
                if not hasS3():
                    self.fields['image_url'] = serializers.CharField(
                        required=False)
        except KeyError:
            pass

    class Meta:
        model = SpellClasses
