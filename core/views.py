from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import serializers


class SuppliersViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return models.Supplier.objects.all()

    def get_serializer_class(self):
        return serializers.SuppliersSerializer
