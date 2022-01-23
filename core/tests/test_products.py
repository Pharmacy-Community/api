import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Product


@pytest.fixture
def add_product(api_client):
    def do_add_product(product):
        return api_client.post('/products/', product)
    return do_add_product


@pytest.mark.django_db
class TestAddProduct:
    test_product = {'name': 'Product Name', 'generic_name': 'Generic Name'}

    required_permissions = ['Can add product']

    @pytest.mark.skip
    def test_anonymous_user_can_not_add_product(self, add_product):
        response = add_product(self.test_product)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_can_not_add_product(self, authenticate, add_product):
        authenticate()
        response = add_product(self.test_product)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_add_product(self, authenticate, add_product):
        authenticate(permissions=self.required_permissions)
        response = add_product(self.test_product)
        # TODO Do more checks, id, name, generic name
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_authorised_user_with_bad_input(self, authenticate, add_product):
        authenticate(permissions=self.required_permissions)
        response = add_product({})
        # TODO asssert exitance of error messages
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_product_name(self, authenticate, add_product):
        existing_product = baker.make(Product)
        authenticate(permissions=self.required_permissions)
        response = add_product({
            'name': existing_product.name,
            'generic_name': existing_product.generic_name
        })
        # TODO Assert error messages
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def view_products(api_client):
    return lambda: api_client.post('/products/')


class TestViewProducts:
    def test_if_anonymous_user_can_not_view_products(self, view_products):
        response = view_products()
