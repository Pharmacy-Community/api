import pytest
from core.models import Purchase, Supplier
from model_bakery import baker
from rest_framework import status


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
def view_supplier(api_client):
    def do_view_supplier(supplier_id):
        return api_client.get(f'/suppliers/{supplier_id}/')
    return do_view_supplier


@pytest.fixture
def delete_supplier(api_client):
    def do_delete_supplier(supplier_id):
        return api_client.delete(f'/suppliers/{supplier_id}/')
    return do_delete_supplier


@pytest.mark.django_db
class TestCreateSupplier():
    required_permissions = ['Can add supplier']

    @pytest.mark.skip
    def test_if_un_authenticated_user_returns_401_UNAUTHORIZED(self, create_supplier):
        response = create_supplier({'name': 'SupplierName'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_returns_403_FORBIDDEN(self, authenticate, create_supplier):
        authenticate()

        response = create_supplier({'name': 'suplier name'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_supplier):
        authenticate(permissions=self.required_permissions)
        # Empty Supplier Name
        response = create_supplier({'name': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_not_add_duplicate_suppliers(self, authenticate, create_supplier):
        # Add Sample Supplier
        supplier = baker.make(Supplier)
        authenticate(permissions=self.required_permissions)

        # Add Supplier with duplicate name
        response = create_supplier({'name': supplier.name})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_create_a_supplier(self, authenticate, create_supplier):
        authenticate(permissions=self.required_permissions)

        response = create_supplier({'name': 'Supplier Name'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestViewSuppliers:
    required_permissions = ['Can view supplier']

    @pytest.mark.skip
    def test_if_un_authenticated_user_can_not_view_suppliers(self, view_suppliers):
        response = view_suppliers()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_with_out_permissions_can_not_view_suppliers(self, authenticate, view_suppliers):
        authenticate()
        response = view_suppliers()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_suppliers(self, authenticate, view_suppliers):
        number_of_sample_suppliers = 5
        # Add Sample Suppliers
        [baker.make(Supplier)for _ in range(number_of_sample_suppliers)]

        authenticate(permissions=self.required_permissions)

        response = view_suppliers()

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == number_of_sample_suppliers


@pytest.mark.django_db
class TestViewSupplier:
    required_permissions = ['Can view supplier']

    @pytest.mark.skip
    def test_if_anonymous_user_can_not_view_supplier(self, view_supplier):
        supplier = baker.make(Supplier)
        response = view_supplier(supplier.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permission_can_not_view_supplier(self, authenticate, view_supplier):
        supplier = baker.make(Supplier)
        authenticate()

        response = view_supplier(supplier.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_supplier(self, authenticate, view_supplier):
        supplier = baker.make(Supplier)
        authenticate(permissions=self.required_permissions)
        response = view_supplier(supplier.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': supplier.id,
            'name': supplier.name,
            'address': supplier.address,
            'contact': supplier.contact
        }

    def test_if_can_not_view_a_supplier_that_does_not_exist(self, authenticate, view_supplier):
        # Add Sample Suppliers
        number_of_sample_suppliers = 5
        [baker.make(Supplier) for _ in range(1, number_of_sample_suppliers+1)]
        authenticate(permissions=self.required_permissions)

        non_existent_supplier_id = number_of_sample_suppliers + 1
        response = view_supplier(non_existent_supplier_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteSupplier:
    required_permissions = ['Can delete supplier']

    @pytest.mark.skip
    def test_if_anonymous_user_can_not_delete_a_supplier(self, delete_supplier):
        supplier = baker.make(Supplier)
        response = delete_supplier(supplier.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_un_authorized_user_can_not_delete_a_supplier(self, authenticate, delete_supplier):
        supplier = baker.make(Supplier)
        authenticate()
        response = delete_supplier(supplier.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_delete_supplier(self, authenticate, delete_supplier):
        supplier = baker.make(Supplier)
        authenticate(permissions=self.required_permissions)

        response = delete_supplier(supplier.id)
        # TODO May need to check if id matches
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_handles_deleting_supplier_that_does_not_exist(self, authenticate, delete_supplier):
        authenticate(permissions=self.required_permissions)
        none_existent_supplier_id = 10
        response = delete_supplier(none_existent_supplier_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.skip
    def test_if_can_not_delete_suppliers_with_purchases(self, authenticate, delete_supplier):
        purchase = baker.make(Purchase)
        supplier = purchase.supplier

        authenticate(permissions=self.required_permissions)

        response = delete_supplier(supplier.id)
        # TODO Fix Bug
        assert response.status_code == status.HTTP_400_BAD_REQUEST
