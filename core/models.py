import imp
import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# TODO Add User profile image
class User(AbstractUser):
    email = models.EmailField(unique=True)


class Account(models.Model):
    ACCOUNT_CATEGORIES = (
        ('SUPPLIER', 'Supplier Account'),
        ('CUSTOMER', 'Customer Account'),
        ('CASH', 'Cash Account'),
        ('BANK', 'Bank Account'),
        ('MOBILE MONEY', 'Mobile Money Account'),
    )
    name = models.CharField(max_length=255,null=False, blank=False)
    category = models.CharField(max_length=255, choices=ACCOUNT_CATEGORIES)
    balance = models.IntegerField()

    def __str__(self) -> str:
        return self.accountitem.id
    
    class Meta:
        ordering=['name', 'id']


class AccountItem(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=13, null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Expense(models.Model):
    date = models.DateField(auto_created=True)
    details = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.details} for {self.amount}"
    
    class Meta:
        ordering=['-date', 'id']


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    generic_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class PackSize(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="pack_sizes")
    units = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.product.name}, {self.units}'s"

    class Meta:
        ordering = ['product__name']


class Purchase(models.Model):
    supplier_id = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    date = models.DateField(auto_created=True)
    invoice = models.CharField(max_length=30)

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def __str__(self) -> str:
        return self.invoice

    class Meta:
        ordering = ['date', '-id']


class Inventory(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)

    batch_number = models.CharField(max_length=20, null=True)
    expiry_date = models.DateField(null=True)

    pack_size = models.PositiveIntegerField()
    pack_cost = models.PositiveIntegerField()
    quantity = models.IntegerField()
    availale_units = models.IntegerField()

    @property
    def total(self):
        return self.pack_cost * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name}, {self.batch_number}:- {5} Left"


class Sale(models.Model):
    # TODO Add Dispenser
    # Payment Method
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_created=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.PROTECT, blank=True, null=True)

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def __str__(self) -> str:
        return f"Sale {self.id}"


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.PROTECT, related_name='items')
    pack_size = models.ForeignKey(
        PackSize, on_delete=models.PROTECT, related_name='pack_size')  # TODO Name Pack Size
    sale_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.quantity * self.pack_size.sale_price

    def __str__(self) -> str:
        return f"{self.pack_size}"


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
