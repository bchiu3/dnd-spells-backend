from django.urls import path
from .views import *

urlpatterns = [
    path("spells/", SpellsView.as_view()),
    path("spells/<str:name>/", SpellsInstanceView.as_view()),
    path("classes/", SpellClassesView.as_view()),
    path("classes/<str:name>/", SpellClassesInstanceView.as_view()),
]