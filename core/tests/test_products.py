import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Product, PackSize

PRODUCTS_ENDPOINT = "/products/"


@pytest.fixture
def add_product(api_client):
    def do_add_product(product):
        return api_client.post(PRODUCTS_ENDPOINT, product)
    return do_add_product


@pytest.mark.django_db
class TestAddProduct:
    test_product = {
        "name": "Product Name",
        "generic_name": "Generic Name",
        "pack_sizes": [
            {
                "units": 10,
                "sale_price": 500
            }
        ]
    }

    required_permissions = ['Can add product']

    def get_sample_test_product(self):
        sample_product = baker.prepare(Product)
        sample_pack_sizes = baker.prepare(PackSize, _quantity=5)
        return {
            "name": sample_product.name,
            "generic_name": sample_product.generic_name,
            "pack_sizes": [
                {
                    "units": pack_size.units,
                    "sale_price": pack_size.sale_price
                }
                for pack_size in sample_pack_sizes
            ]
        }

    def test_anonymous_user_can_not_add_product(self, add_product):
        response = add_product(self.test_product)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_can_not_add_product(self, authenticate, add_product):
        authenticate()
        response = add_product(self.test_product)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_add_product(self, authenticate, add_product):
        authenticate(permissions=self.required_permissions)
        product = self.get_sample_test_product()
        response = add_product(product)
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
    def do_view_products():
        return api_client.get(PRODUCTS_ENDPOINT)
    return do_view_products


class TestViewProducts:
    def test_if_anonymous_user_can_not_view_products(self, view_products):
        response = view_products()
