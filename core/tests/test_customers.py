import pytest
from core.models import Customer, Sale
from model_bakery import baker
from rest_framework import status


CUSTOMERS_ENDPOINT = "/customers/"

@pytest.fixture
def create_customer(api_client):
    def do_create_customer(customer):
        return api_client.post(CUSTOMERS_ENDPOINT, customer)
    return do_create_customer


@pytest.fixture
def view_customers(api_client):
    def do_view_customers():
        return api_client.get(CUSTOMERS_ENDPOINT)
    return do_view_customers


@pytest.fixture
def view_customer(api_client):
    def do_view_customer(customer_id):
        return api_client.get(f'{CUSTOMERS_ENDPOINT}{customer_id}/')
    return do_view_customer


@pytest.fixture
def delete_customer(api_client):
    def do_delete_customer(customer_id):
        return api_client.delete(f'{CUSTOMERS_ENDPOINT}{customer_id}/')
    return do_delete_customer


@pytest.mark.django_db
class TestCreateCustomer():
    required_permissions = ['Can add customer']
    sample_customer = {
        "name":"Sample Customer",
        "address":"Kampala",
        "contanct":"0000000000"
    }

    def test_if_un_authenticated_user_returns_401_UNAUTHORIZED(self, create_customer):
        response = create_customer(self.sample_customer)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_returns_403_FORBIDDEN(self, authenticate, create_customer):
        authenticate()

        response = create_customer(self.sample_customer)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_customer):
        authenticate(permissions=self.required_permissions)
        # Empty Customer Name
        response = create_customer({'name': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_not_add_duplicate_customers(self, authenticate, create_customer):
        # Add Sample Customer
        customer = baker.make(Customer)
        authenticate(permissions=self.required_permissions)

        # Add Customer with duplicate name
        duplicate_customer = self.sample_customer
        duplicate_customer["name"] = customer.name
        response = create_customer(duplicate_customer)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_can_create_a_customer(self, authenticate, create_customer):
        authenticate(permissions=self.required_permissions)

        response = create_customer(self.sample_customer)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestViewCustomers:
    required_permissions = ['Can view customer']

    def test_if_un_authenticated_user_can_not_view_customers(self, view_customers):
        response = view_customers()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_with_out_permissions_can_not_view_customers(self, authenticate, view_customers):
        authenticate()
        response = view_customers()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_customers(self, authenticate, view_customers):
        number_of_sample_customers = 5
        # Add Sample Customers
        [baker.make(Customer)for _ in range(number_of_sample_customers)]

        authenticate(permissions=self.required_permissions)

        response = view_customers()

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == number_of_sample_customers


@pytest.mark.django_db
class TestViewCustomer:
    required_permissions = ['Can view customer']

    @pytest.mark.skip
    def test_if_anonymous_user_can_not_view_customer(self, view_customer):
        customer = baker.make(Customer)
        response = view_customer(customer.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permission_can_not_view_customer(self, authenticate, view_customer):
        customer = baker.make(Customer)
        authenticate()

        response = view_customer(customer.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_customer(self, authenticate, view_customer):
        customer = baker.make(Customer)
        authenticate(permissions=self.required_permissions)
        response = view_customer(customer.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': customer.id,
            'name': customer.name,
            'address': customer.address,
            'contact': customer.contact
        }

    def test_if_can_not_view_a_customer_that_does_not_exist(self, authenticate, view_customer):
        # Add Sample Customers
        number_of_sample_customers = 5
        [baker.make(Customer) for _ in range(1, number_of_sample_customers+1)]
        authenticate(permissions=self.required_permissions)

        non_existent_customer_id = number_of_sample_customers + 1
        response = view_customer(non_existent_customer_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCustomer:
    required_permissions = ['Can delete customer']

    @pytest.mark.skip
    def test_if_anonymous_user_can_not_delete_a_customer(self, delete_customer):
        customer = baker.make(Customer)
        response = delete_customer(customer.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_un_authorized_user_can_not_delete_a_customer(self, authenticate, delete_customer):
        customer = baker.make(Customer)
        authenticate()
        response = delete_customer(customer.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_delete_customer(self, authenticate, delete_customer):
        customer = baker.make(Customer)
        authenticate(permissions=self.required_permissions)

        response = delete_customer(customer.id)
        # TODO May need to check if id matches
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_handles_deleting_customer_that_does_not_exist(self, authenticate, delete_customer):
        authenticate(permissions=self.required_permissions)
        none_existent_customer_id = 10
        response = delete_customer(none_existent_customer_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.skip
    def test_if_can_not_delete_customers_with_purchases(self, authenticate, delete_customer):
        sale = baker.make(Sale)
        customer = sale.customer

        authenticate(permissions=self.required_permissions)

        response = delete_customer(customer.id)
        # TODO Fix Bug
        assert response.status_code == status.HTTP_400_BAD_REQUEST
