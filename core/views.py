from rest_framework import viewsets
from . import models
from . import serializers


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SuppliersSerializer


class PurchasesViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return models.Purchase.objects.all()

    def get_serializer_class(self):
        return serializers.PurchasesSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductsSerializer
