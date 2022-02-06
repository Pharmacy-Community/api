from rest_framework import routers
from django.urls import path, include
from . import views
router = routers.DefaultRouter()

router.register(r'accounts', views.AccountsViewSet, basename='accounts')
router.register(r'customers', views.CustomersViewSet, basename='customers')
router.register(r'expenses', views.ExpensesViewSet, basename='expenses')
router.register(r'groups', views.GroupsViewSet, basename='groups')
router.register(r'products', views.ProductsViewSet, basename='products')
router.register(r'purchases', views.PurchasesViewSet, basename='purchases')
router.register(r'sales', views.SalesViewSet, basename='sales')
router.register(r'suppliers', views.SuppliersViewSet, basename='suppliers')
router.register(r'users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
