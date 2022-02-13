from urllib import response
import pytest
from rest_framework import status
from model_bakery import baker

from core.models import Account, Expense


EXPENSES_ENDPOINT = "/expenses/"


@pytest.fixture
def create_expense(api_client):
    def do_create_expense(expense):
        return api_client.post(EXPENSES_ENDPOINT, expense)
    return do_create_expense


@pytest.fixture
def view_expense(api_client):
    def do_view_expense(expense_id):
        return api_client.get(f"{EXPENSES_ENDPOINT}{expense_id}/")
    return do_view_expense


@pytest.fixture
def view_expenses(api_client):
    def do_view_expenses():
        return api_client.get(EXPENSES_ENDPOINT)
    return do_view_expenses


@pytest.mark.django_db
class TestAddExpense:
    required_permissions = ["Can add expense"]
    sample_test_expense_with_out_account_id = {
        "date": "2021-01-01",
        "details": "Sample Expense",
        "amount": 5000
    }

    def get_sample_test_expense(self):
        # Add the test Account
        account = baker.make(Account)
        self.sample_test_expense_with_out_account_id["account_id"] = account.id
        return self.sample_test_expense_with_out_account_id

    def test_anonymous_user_can_not_create_expense(self, create_expense):
        sample_test_expense = self.get_sample_test_expense()
        response = create_expense(sample_test_expense)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_can_not_create_expense(self, authenticate, create_expense):
        sample_test_expense = self.get_sample_test_expense()
        authenticate()
        response = create_expense(sample_test_expense)

        # TODO if user can not add expense on account they dont have permissions

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_not_create_expense_with_incomplete_data(self, authenticate, create_expense):
        authenticate(permissions=self.required_permissions)
        # User can not add expense without account
        expense = self.sample_test_expense_with_out_account_id
        response = create_expense(expense)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # TODO if user can not add expense with a non expense account i.e Supplier Account, or Customer Account

    def test_if_authorised_user_can_create_expense(self, authenticate, create_expense):
        authenticate(permissions=self.required_permissions)
        sample_expense = self.get_sample_test_expense()

        response = create_expense(sample_expense)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestViewExpense:
    required_permissions = ["Can view expense"]

    def add_sample_expense_to_db(self):
        return baker.make(Expense)

    def test_if_anonymous_user_can_not_view_expense(self, view_expense):
        sample_db_expense = self.add_sample_expense_to_db()
        response = view_expense(sample_db_expense.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_without_permissions_can_not_view_expense(self, authenticate, view_expense):
        authenticate()
        sample_db_expense = self.add_sample_expense_to_db()
        response = view_expense(sample_db_expense.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_not_view_non_existent_expense(self, authenticate, view_expense):
        authenticate(permissions=self.required_permissions)
        non_existent_expense_id = 1
        response = view_expense(non_existent_expense_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_authorised_user_can_view_expense(self, authenticate, view_expense):
        authenticate(permissions=self.required_permissions)
        sample_db_expense = self.add_sample_expense_to_db()
        response = view_expense(sample_db_expense.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'id': 1,
            'date': str(sample_db_expense.date),
            'account_id': sample_db_expense.account.id,
            "details": sample_db_expense.details,
            "amount": sample_db_expense.amount
        }


@pytest.mark.django_db
class TestViewExpenses:

    required_permissions = ["Can view expense"]

    def make_sample_expenses(self):
        number_of_sample_expenses = 5
        return [baker.make(Expense) for _ in range(number_of_sample_expenses)]

    def test_if_anonymous_user_can_not_view_expenses(self, view_expenses):
        self.make_sample_expenses()
        response = view_expenses()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticates_user_without_permissions_can_not_view_expenses(self, authenticate, view_expenses):
        authenticate()
        self.make_sample_expenses()
        response = view_expenses()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_authorised_user_can_view_expenses(self, authenticate, view_expenses):
        authenticate(permissions=self.required_permissions)
        self.make_sample_expenses()
        response = view_expenses()
        assert response.status_code == status.HTTP_200_OK
