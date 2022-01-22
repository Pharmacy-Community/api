import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(**kwargs):
        user = get_user_model()()
        # Save the user incase of adding permissions
        user.save()

        # Add Properties to user
        for permission in kwargs.get('permissions', []):
            user_permission = Permission.objects.get(name=permission)
            user.user_permissions.add(user_permission)

        return api_client.force_authenticate(user=user)
    return do_authenticate
