import pytest
from rest_framework import status


@pytest.fixture
def create_purchase(api_client):
    def do_create_purchase(purchase):
        return api_client.post('/purchases/', purchase)
    return do_create_purchase


class TestCreatePurchase:
    @pytest.mark.skip
    def test_un_authenticated_user_returns_401(self, create_purchase):
        response = create_purchase({'invoice': '123'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Assert that there is an error message
        assert response.data is not None

    @pytest.mark.skip
    def test_if_un_authorised_user_returns_403(self, authenticate, create_purchase):
        authenticate()

        response = create_purchase({'invoice': '123'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data is not None

    def test_if_authorised_user_with_bad_input_returns_400(self, authenticate, create_purchase):
        authenticate(permissions=['can_add_purchase'])

        response = create_purchase({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data is not None

    def test_if_authorised_user_returns_201(self, authenticate, create_purchase):
        authenticate(permissions=['can_add_purchase'])
        response = create_purchase({'invoice': '1234'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
