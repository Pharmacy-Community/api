from rest_framework import serializers
from . import models


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ['id', 'name', 'address', 'contact']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Purchase
        # TODO Add Purchase Items
        fields = ['id', 'date', 'invoice', 'supplier']
