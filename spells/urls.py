from django.urls import path, register_converter
from .views import *
from . import converters

register_converter(converters.StringConverter, "string")

urlpatterns = [
    path("spells/", SpellsView.as_view()),                              #URL for spell lists
    path("spells/<string:name>/", SpellsInstanceView.as_view()),        #URL for individual spell
    path("spells/id/<string:_id>/", SpellsInstanceViewId.as_view()),        #URL for individual spell with id
    path("feats/", FeatsView.as_view()),                              #URL for spell lists
    path("feats/<string:name>/", FeatsInstanceView.as_view()),        #URL for individual spell
    path("classes/", SpellClassesView.as_view()),                       #URL for classes
    path("classes/<string:name>/", SpellClassesInstanceView.as_view()), #URL for individual class
]