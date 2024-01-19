from re import search
from django.shortcuts import render
from rest_framework import generics
from .serializers import SpellClassSerializer, SpellSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
import django_mongoengine_filter as filters
import django_filters
from rest_framework.parsers import MultiPartParser, FileUploadParser

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50

class SpellFilter(filters.FilterSet):
    name = filters.StringFilter(lookup_type='icontains')
    description = filters.StringFilter(lookup_type='icontains')
    component_material = filters.StringFilter(lookup_type='icontains')
    classes = filters.StringFilter(lookup_type='iexact')
    components = filters.StringFilter(lookup_type='icontains')
    spell_range = filters.StringFilter(lookup_type='icontains')
    school = filters.StringFilter(lookup_type='iexact')
    cast_type = filters.StringFilter(lookup_type='icontains')
    class Meta:
        model = Spells
        fields = [*Spells._fields.keys()] # type: ignore
    
    def filter_classes(self, queryset, name, value):
        return queryset.filter(classes__icontains=value)
            
class SpellsView(generics.ListAPIView):
    queryset = Spells.objects.all() # type: ignore
    serializer_class = SpellSerializer
    pagination_class = StandardResultsSetPagination
    def filter_queryset(self, queryset):
        filter_qs = SpellFilter(self.request.query_params, queryset=queryset) # type: ignore
        return filter_qs.qs

class SpellClassesView(generics.ListCreateAPIView):
    queryset = SpellClasses.objects.all() # type: ignore
    serializer_class = SpellClassSerializer
    parser_classes = (MultiPartParser, FileUploadParser)

class SpellClassesInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpellClasses.objects.all() # type: ignore
    serializer_class = SpellClassSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    lookup_field = 'name'

class SpellsInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spells.objects.all() # type: ignore
    serializer_class = SpellSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    lookup_field = 'name'