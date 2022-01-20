from re import search
from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['balance']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'address']
    search_fields = ['name']


@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'details', 'amount']
    list_filter = ['date']


class PackSizeInline(admin.TabularInline):
    model = models.PackSize
    extra = 1
    min_num = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'pack_sizes']
    search_fields = ['name', 'generic_name']
    inlines = [PackSizeInline]
    # TODO Add filter by dosage form

    def pack_sizes(self, product):
        return ", ".join([f"{pack_size.units}'s" for pack_size in product.pack_sizes.all()])


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_filter = ['expiry_date']
    list_display = ['product', 'batch_number',
                    'expiry_date', 'pack_cost', 'quantity']


class InventoryInline(admin.TabularInline):
    model = models.Inventory
    extra = 1
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):

        formset = super().get_formset(request, obj, **kwargs)
        product = formset.form.base_fields['product']

        product.widget.can_add_related = False
        product.widget.can_delete_related = False
        product.widget.can_change_related = False

        return formset


@admin.register(models.PackSize)
class PackSizeAdmin(admin.ModelAdmin):
    search_fields = ['product__name__istartswith', 'product__name__icontains']
    list_display = ['id', '__str__', 'sale_price']
    list_editable = ['sale_price']


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ['id', 'date', 'invoice', 'supplier', 'total']
    inlines = [InventoryInline]
    search_fields = ['invoice__exact',
                     'supplier__name__icontains']

    autocomplete_fields = ['supplier']

    def total(self, purchase):
        return purchase.total

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        supplier = form.base_fields["supplier"]

        supplier.widget.can_delete_related = False
        supplier.widget.can_change_related = False

        return form


class SaleItemInline(admin.TabularInline):
    model = models.SaleItem
    autocomplete_fields = ['pack_size']
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):

        formset = super().get_formset(request, obj, **kwargs)
        pack_size = formset.form.base_fields['pack_size']

        pack_size.widget.can_add_related = False
        pack_size.widget.can_delete_related = False
        pack_size.widget.can_change_related = False

        return formset


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'date', 'customer', 'total']
    inlines = [SaleItemInline]
    list_filter = ['date']
    search_fields = ['customer__name__icontains']

    def total(self, sale):
        return sale.total

    def get_form(self, request, obj=None, **kwargs):

        form = super().get_form(request, obj, **kwargs)
        supplier = form.base_fields["customer"]

        supplier.widget.can_delete_related = False
        supplier.widget.can_change_related = False

        return form


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'address']
    search_fields = ['name']
