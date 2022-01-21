import pytest
from rest_framework import status


@pytest.fixture
def create_supplier(api_client):
    def do_create_supplier(supplier):
        return api_client.post('/suppliers/', supplier)
    return do_create_supplier


@pytest.mark.django_db
class TestCreateSupplier():
    @pytest.mark.skip
    def test_if_un_authenticated_user_returns_401(self, create_supplier):
        response = create_supplier({'name': 'SupplierName'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    def test_if_un_authorised_user_returns_403(self, authenticate, create_supplier):
        authenticate()

        response = create_supplier({'name': 'suplier name'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_supplier):
        authenticate(is_staff=True)

        response = create_supplier({'name': ''})  # Empty Supplier Name

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_returns_201(self, authenticate, create_supplier):
        authenticate(is_staff=True)

        response = create_supplier({'name': 'Supplier Name'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
