from rest_framework import serializers
from . import models


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ['id', 'name', 'address', 'contact']
