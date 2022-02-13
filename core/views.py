from django.contrib.auth.models import Group
from rest_framework import viewsets
from . import models
from . import serializers


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountsSerializer
    filter_fields = ['name', 'category']


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomersSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = models.Expense.objects.all()
    serializer_class = serializers.ExpensesSerializer
    # TODO Add date range, account, entrant
    filterset_fields = ['account_id']
    search_fields = ['details']


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer
    filterset_fields = ['product_id']


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchasesSerializer
    filterset_fields = ["supplier_id", "invoice"]
    search_fields = ['invoice']


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductsSerializer


class SalesViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SalesSerializer
    filter_fields = ['date', 'customer_id']


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SuppliersSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UsersSerializer
