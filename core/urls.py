from rest_framework import routers
from django.urls import path, include
from . import views
router = routers.DefaultRouter()

router.register('accounts', views.AccountsViewSet, basename='accounts')
router.register('customers', views.CustomersViewSet, basename='customers')
router.register('expenses', views.ExpensesViewSet, basename='expenses')
router.register('groups', views.GroupsViewSet, basename='groups')
router.register('inventory', views.InventoryViewSet, basename='inventory')
router.register('products', views.ProductsViewSet, basename='products')
router.register('purchases', views.PurchasesViewSet, basename='purchases')
router.register('sales', views.SalesViewSet, basename='sales')
router.register('suppliers', views.SuppliersViewSet, basename='suppliers')
router.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
