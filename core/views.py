from django.contrib.auth.models import Group
from rest_framework import viewsets

from core.filters import ExpensesFilter
from . import models
from . import serializers
from . import filters


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountsSerializer
    filterset_class = filters.AccountsFilter
    search_fields = ["name"]
    ordering_fields = "__all__"


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomersSerializer
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = "__all__"


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = models.Expense.objects.all()
    serializer_class = serializers.ExpensesSerializer
    filterset_class = ExpensesFilter
    search_fields = ['details']
    ordering_fields = "__all__"


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    search_fields = ["name"]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer
    filterset_fields = ['product_id', 'batch_number']


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchasesSerializer
    filterset_class = filters.PurchasesFilter
    search_fields = ['invoice']


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductsSerializer
    search_fields = ['name', 'generic_name']


class SalesViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SalesSerializer
    filterset_class = filters.SalesFilter
    search_fields = ['id']


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SuppliersSerializer
    search_fields = ['name']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UsersSerializer
    search_fields = ["first_name", "last_name"]
