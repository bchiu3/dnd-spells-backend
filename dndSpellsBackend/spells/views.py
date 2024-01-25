from re import search
from django.shortcuts import render
from rest_framework import generics
from .serializers import SpellClassSerializer, SpellSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
import django_mongoengine_filter as filters
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50

class SpellFilter(filters.FilterSet):
    name = filters.StringFilter(lookup_type='icontains')
    description = filters.StringFilter(lookup_type='icontains')
    component_material = filters.StringFilter(lookup_type='icontains')
    classes = filters.MethodFilter(action='filter_classes')
    components = filters.StringFilter(lookup_type='icontains')
    spell_range = filters.StringFilter(lookup_type='icontains')
    school = filters.MethodFilter(lookup_type='filter_school')
    range_type = filters.StringFilter(lookup_type='iexact')
    level = filters.MethodFilter(action='filter_level')
    components = filters.MethodFilter(action='filter_components')
    cast_type = filters.MethodFilter(action='filter_cast_type')

    class Meta:
        model = Spells
        fields = [*Spells._fields.keys()] # type: ignore
    
    def filter_level(self, queryset, name, value):
        values = value.split(",")
        return queryset(level__in=values)
    
    def filter_school(self, queryset, name, value):
        values = value.split(",")
        return queryset(school__in=values)
    
    def filter_classes(self, queryset, name, value):
        values = value.lower().split(",")
        return queryset(classes__in=values)
    
    def filter_components(self, queryset, name, value):
        values = value.title().split(",")
        return queryset(components__in=values)
    
    def filter_cast_type(self, queryset, name, value):
        values = value.title().split(",")
        return queryset(cast_type__in=values)

class SpellsView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Spells.objects.all() # type: ignore
    serializer_class = SpellSerializer
    pagination_class = StandardResultsSetPagination
    def filter_queryset(self, queryset):
        filter_qs = SpellFilter(self.request.query_params, queryset=queryset) # type: ignore
        return filter_qs.qs.order_by('level', '-is_recommended', 'name')

class SpellsInstanceView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Spells.objects.all() # type: ignore
    serializer_class = SpellSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    lookup_field = 'name'
    
class SpellClassesView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SpellClasses.objects.all() # type: ignore
    serializer_class = SpellClassSerializer
    parser_classes = (MultiPartParser, FileUploadParser)

class SpellClassesInstanceView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SpellClasses.objects.all() # type: ignore
    serializer_class = SpellClassSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    lookup_field = 'name'
    
        
    
