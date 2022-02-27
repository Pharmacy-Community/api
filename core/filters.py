import django_filters
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from . import models


class AccountsFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = models.Account
        fields = ['date', 'name', 'category']


class ExpensesFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = models.Expense
        fields = ['account_id', 'date']


class PurchasesFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = models.Purchase
        fields = ['date', 'supplier_id', 'invoice']


class SalesFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = models.Expense
        fields = ['date', 'account_id']
