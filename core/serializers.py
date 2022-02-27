from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from . import models


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "name", "category", "balance"]


class AccountItemSerializer(serializers.ModelSerializer):
    account = AccountsSerializer()

    class Meta:
        model = models.AccountItem
        fields = ["id", "account"]


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ["id", "name", "address", "contact", "account_id"]


class ExpenseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ["id", "name"]


class ExpensesSerializer(serializers.ModelSerializer):
    account_id = serializers.IntegerField()

    class Meta:
        model = models.Expense
        fields = ["id", "date", "details", "amount", "account_id"]

    def create(self, validated_data):
        account_id = validated_data.pop("account_id")
        account = get_object_or_404(models.Account, id=account_id)
        validated_data["account"] = account
        expense = models.Expense.objects.create(**validated_data)
        expense.save()
        return expense


class GroupUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id']


class GroupSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects.all(),
        source="user_set"

    )
    # users = GroupUsersSerializer(many=True)

    class Meta:
        model = Group
        fields = ["id", "name", "users"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ["id", "purchase_id", "product_id", "batch_number", "expiry_date", "pack_size",
                  "pack_cost", "quantity", "available_units"
                  ]


class PackSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackSize
        fields = ["units", "sale_price"]


class ProductsSerializer(WritableNestedModelSerializer):
    pack_sizes = PackSizesSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ["id", "name", "generic_name", "pack_sizes"]


class PurchaseItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ["id", "product_id", "batch_number",
                  "expiry_date", "pack_size", "pack_cost", "quantity"]


class PurchasesSerializer(serializers.ModelSerializer):
    items = PurchaseItemsSerializer(many=True)
    supplier_id = serializers.IntegerField(source='supplier.id')

    class Meta:
        model = models.Purchase
        fields = ["id", "date", "invoice", "total", "items", "supplier_id"]

    def validate(self, data):
        if data["total"] == sum([item["pack_cost"]*item["quantity"] for item in data["items"]]):
            return data
        raise serializers.ValidationError(
            "The total of the invoice does not match the total of the items")

    def create(self, validated_data):
        supplier_account = validated_data["supplier"].account
        supplier_account.balance -= validated_data["total"]
        supplier_account.save()
        serializer_items = validated_data.pop("items")
        items = [
            models.Inventory(
                **item
            )
            for item in serializer_items
        ]

        validated_data["items"] = items

        purchase = models.Purchase.objects.create(**validated_data)
        purchase.save()
        return purchase


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = ["id", "date", "customer_id", "items"]


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ["id", "name", "address", "contact", "account_id"]


class UsersSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all()
    )
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            "id", "full_name", "first_name", "last_name", "username", "is_active",
            "email", "groups", "user_permissions", "is_superuser"
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()
