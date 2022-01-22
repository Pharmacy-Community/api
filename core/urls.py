from rest_framework import routers
from django.urls import path, include
from . import views
router = routers.DefaultRouter()
router.register(r'suppliers', views.SuppliersViewSet, basename='suppliers')
router.register(r'purchases', views.PurchasesViewSet, basename='purchases')
router.register(r'products', views.ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
