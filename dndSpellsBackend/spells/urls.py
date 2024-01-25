from django.urls import path, register_converter
from .views import *
from . import converters

register_converter(converters.StringConverter, "string")

urlpatterns = [
    path("spells", SpellsView.as_view()),
    path("spells/<string:name>", SpellsInstanceView.as_view()),
    path("spells/<string:name>/", SpellsInstanceView.as_view()),
    path("classes", SpellClassesView.as_view()),
    path("classes/<string:name>", SpellClassesInstanceView.as_view()),
]