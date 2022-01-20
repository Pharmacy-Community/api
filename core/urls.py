from rest_framework import routers
from django.urls import path, include
from .views import SuppliersViewSet

router = routers.DefaultRouter()
router.register(r'suppliers', SuppliersViewSet, basename='suppliers')

urlpatterns = [
    path('', include(router.urls)),
]
