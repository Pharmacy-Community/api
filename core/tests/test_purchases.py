import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Supplier
from datetime import datetime


@pytest.fixture
def create_purchase(api_client):
    def do_create_purchase(purchase):
        return api_client.post('/purchases/', purchase)
    return do_create_purchase


@pytest.mark.django_db
class TestCreatePurchase:
    @pytest.mark.skip
    def test_if_un_authenticated_user_can_not_create_a_purchase(self, create_purchase):
        response = create_purchase({'invoice': '123'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Assert that there is an error message
        assert response.data is not None

    def test_if_un_authorised_user_without_permissions_can_not_create_a_purchase(self, authenticate, create_purchase):
        authenticate()

        response = create_purchase({'invoice': '123'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data is not None

    def test_if_authorised_user_with_bad_input_returns_400_BAD_REQUEST(self, authenticate, create_purchase):
        authenticate(permissions=['Can add purchase'])

        response = create_purchase({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_can_create_a_purchase(self, authenticate, create_purchase):
        # Add Supplier
        supplier = baker.make(Supplier)
        authenticate(permissions=['Can add purchase'])

        purchase = {
            'date': str(datetime.now().date()),
            'invoice': '123',
            'supplier': supplier.id
        }
        # TODO Add Items

        response = create_purchase(purchase)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
