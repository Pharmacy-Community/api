import pytest
from model_bakery import baker
from rest_framework import status

from core.models import Supplier


@pytest.fixture
def create_supplier(api_client):
    def do_create_supplier(supplier):
        return api_client.post('/suppliers/', supplier)
    return do_create_supplier


@pytest.fixture
def view_suppliers(api_client):
    def do_view_suppliers():
        return api_client.get('/suppliers/')
    return do_view_suppliers


@pytest.fixture
def get_supplier(api_client):
    def do_get_supplier(supplier_id):
        return api_client.get(f'/suppliers/{supplier_id}/')
    return do_get_supplier


@pytest.fixture
def set_up_get_supplier():
    return baker.make(Supplier)


@pytest.mark.django_db
class TestCreateSupplier():
    @pytest.mark.skip
    def test_if_un_authenticated_user_returns_401_UNAUTHORIZED(self, create_supplier):
        response = create_supplier({'name': 'SupplierName'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_returns_403_FORBIDDEN(self, authenticate, create_supplier):
        authenticate()

        response = create_supplier({'name': 'suplier name'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_supplier):
        authenticate(permissions=['Can add supplier'])
        # Empty Supplier Name
        response = create_supplier({'name': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_not_add_duplicate_suppliers(self, authenticate, create_supplier):
        # Add Sample Supplier
        supplier = baker.make(Supplier)
        authenticate(permissions=['Can add supplier'])

        # Add Supplier with duplicate name
        response = create_supplier({'name': supplier.name})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_create_a_supplier(self, authenticate, create_supplier):
        authenticate(permissions=['Can add supplier'])

        response = create_supplier({'name': 'Supplier Name'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestViewSupplier:
    @pytest.mark.skip
    def test_if_un_authenticated_user_can_not_view_suppliers(self, view_suppliers):
        response = view_suppliers()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_with_out_permissions_can_not_view_suppliers(self, authenticate, view_suppliers):
        authenticate()
        response = view_suppliers()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_suppliers(self, authenticate, view_suppliers):
        # TODO Add Sample Suppliers
        authenticate(permissions=['Can view supplier'])
        response = view_suppliers()
        assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def delete_supplier(api_client):
    def do_delete_supplier(supplier_id):
        return api_client.delete(f'/suppliers/{supplier_id}/')
    return do_delete_supplier


@pytest.mark.django_dbb
class TestDeleteSupplier:

    def add_sample_supplier(self):
        return baker.make(Supplier)

    def test_if_un_authenticated_user_can_not_delete_supplier(self, delete_supplier):
        pass
# Add Supplier

# Test Delete Supplier
# No permissions
# With purchases
# Does not exist
# Success
