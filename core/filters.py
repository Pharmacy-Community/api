from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from . import models

# TODO Add date range, account, entrant


class ExpensesFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = models.Expense
        fields = ['account_id', 'date']
