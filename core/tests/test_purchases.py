import pytest
from rest_framework import status
from model_bakery import baker
from core.models import Purchase, Supplier, Inventory
from datetime import datetime


@pytest.fixture
def create_purchase(api_client):
    def do_create_purchase(purchase):
        return api_client.post('/purchases/', purchase)
    return do_create_purchase


@pytest.mark.django_db
class TestCreatePurchase:
    required_permissions = ['Can add purchase']

    def get_sample_test_purchase(self):
        supplier = baker.make(Supplier)
        number_of_items = 5
        products = baker.make('Product', _quantity=number_of_items)

        purchase_items = []
        purchase_total = 0

        for product in products:
            inventory_item = baker.prepare(Inventory)
            purchase_total += inventory_item.total
            purchase_items.append({
                'product_id': product.id,
                'batch_number': inventory_item.batch_number,
                'expiry_date': str(inventory_item.expiry_date),
                'pack_size': inventory_item.pack_size,
                'pack_cost': inventory_item.pack_cost,
                'quantity': inventory_item.quantity
            })

        model_purchase = baker.prepare(Purchase)

        return {
            'date': str(model_purchase.date),
            'invoice': model_purchase.invoice,
            'supplier': supplier.id,
            'total': model_purchase.total,
            'items': purchase_items
        }

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
        authenticate(permissions=self.required_permissions)
        purchase = self.get_sample_test_purchase()

        response = create_purchase(purchase)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.fixture
def view_purchases(api_client):
    def do_view_purchases():
        return api_client.get('/purchases/')
    return do_view_purchases


@pytest.mark.django_db
class TestViewPurchases:

    def test_if_anonymous_user_can_not_view_purchases(self, view_purchases):
        response = view_purchases()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_with_out_permissions_can_not_view_purchases(self, authenticate, view_purchases):
        authenticate()
        response = view_purchases()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_pruchases(self, authenticate, view_purchases):
        # TODO Add sample purchases
        authenticate(permissions=['Can view purchase'])
        response = view_purchases()

        assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def view_purchase(api_client):
    def do_view_purchase(purchase_id):
        return api_client.get(f'/purchases/{purchase_id}/')
    return do_view_purchase


@pytest.mark.django_db
class TestViewPurchase:
    def test_if_anonymous_user_can_not_view_purchase(self, view_purchase):
        purchase = baker.make(Purchase)
        response = view_purchase(purchase.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_can_not_view_purchase(self, authenticate, view_purchase):
        purchase = baker.make(Purchase)
        authenticate()
        response = view_purchase(purchase.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorized_user_can_view_purchase(self, authenticate, view_purchase):
        purchase = baker.make(Purchase)
        authenticate(permissions=['Can view purchase'])
        response = view_purchase(purchase.id)
        assert response.status_code == status.HTTP_200_OK
        # TODO Add More fields
        assert response.data == {
            'id': purchase.id,
            'date': str(purchase.date),
            'invoice': purchase.invoice,
            'items': [],
            'supplier_id': purchase.supplier_id,
            'total': purchase.total
        }
