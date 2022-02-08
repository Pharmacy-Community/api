from django.contrib.auth.models import Group
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from . import models


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'name', 'category', 'balance']
    
class AccountItemSerializer(serializers.ModelSerializer):
    account = AccountsSerializer()
    class Meta:
        model = models.AccountItem
        fields = ['id', 'account']


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'name', 'address', 'contact']



class ExpenseAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'name']

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = ['id', 'date', 'details', 'amount', 'account_id']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields= ['id', 'purchase_id', 'product_id','batch_number', 'expiry_date', 'pack_size',
        'pack_cost', 'quantity','available_units'
        ]

class PackSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackSize
        fields = ['units', 'sale_price']


class ProductsSerializer(WritableNestedModelSerializer):
    pack_sizes = PackSizesSerializer(many=True)
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'generic_name', 'pack_sizes']



class PurchaseItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ['id', 'product_id', 'batch_number','expiry_date', 'pack_size','pack_cost','quantity']

class PurchasesSerializer(WritableNestedModelSerializer):
    items = PurchaseItemsSerializer(many=True)
    class Meta:
        model = models.Purchase
        fields = ['id', 'date', 'invoice', 'supplier_id','total', 'items']
    
    def validate(self, data):
        if data['total'] == sum([item['pack_cost']*item['quantity'] for item in data["items"]]):
            return data
        raise serializers.ValidationError("The total of the invoice does not match the total of the items")
    

    def create(self, validated_data):
        # Create a purchase
        # Reduce the supplier account
        supplier = validated_data["supplier"]
        supplier_account = supplier.account
        supplier_account.balance=validated_data.total
        supplier_account.save()
        purchase = super()
        return purchase


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = ['id', 'date', 'customer_id']


class SuppliersSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField()
    class Meta:
        model = models.Supplier
        fields = ['id', 'name', 'address', 'contact', 'account_id']
    
    def get_account_id(self, supplier):
        return supplier.account_id.id



class UsersSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.User
        fields = ["id", "first_name", "last_name", "username", "is_active",
                  "email", "groups", "user_permissions", "is_superuser"]
