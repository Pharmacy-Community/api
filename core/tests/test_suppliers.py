import pytest
from model_bakery import baker
from rest_framework import status

from core.models import Supplier


@pytest.fixture
def create_supplier(api_client):
    def do_create_supplier(supplier):
        return api_client.post('/suppliers/', supplier)
    return do_create_supplier


@pytest.mark.django_db
class TestCreateSupplier():
    def test_if_un_authenticated_user_returns_401(self, create_supplier):
        response = create_supplier({'name': 'SupplierName'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_un_authorised_user_returns_403(self, authenticate, create_supplier):
        authenticate()

        response = create_supplier({'name': 'suplier name'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_supplier):
        authenticate(permissions=['Can add supplier'])

        response = create_supplier({'name': ''})  # Empty Supplier Name

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_returns_201(self, authenticate, create_supplier):
        authenticate(permissions=['Can add supplier'])

        response = create_supplier({'name': 'Supplier Name'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.fixture
def get_supplier(api_client):
    def do_get_supplier(supplier_id):
        return api_client.get(f'/suppliers/{supplier_id}/')
    return do_get_supplier


@pytest.fixture
def set_up_get_supplier():
    return baker.make(Supplier)


@pytest.mark.django_db
class TestViewSupplier:
    def test_if_supplier_exists_returns_200(self, api_client, set):
        assert False
