import pytest
from django.test import TestCase, RequestFactory
from pytest_django.asserts import assertTemplateUsed

from app.models import WalletUser
from app.views import sign_in


class FinanceViewTestCases(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        user = WalletUser(email="test@mail.ru", name="Тестер")
        user.set_password('password')
        user.save()
        self.user = user

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_login_view(self):
        request = self.factory.post("/sign_in/")
        request.user = self.user
        # Todo проверить, что нам вернется main page
        response = sign_in(request)
        self.assertTemplateUsed(template_name='main.html')

    #
    # def test_create_cocktail_view(self):
    #     request = self.factory.get("")
    #     request.user = self.user
    #     response = CreateCocktail.as_view()(request)
    #     self.assertEqual(response.status_code, 200)


@pytest.fixture
def create_user(db):
    def make_user():
        return WalletUser.objects.create(
            email='test@test.com', password='test_password'
        )
    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user):
    def make_auto_login():
        user = create_user()
        client.login(email=user.email, password=user.password)
        return client, user
    return make_auto_login


@pytest.mark.django_db
def test_logout_logged(auto_login_user):
    client, _ = auto_login_user()
    client.get('/logout/')
    assertTemplateUsed(template_name='main.html')


@pytest.mark.parametrize('url', ['/logout/', '/new_note/', '/receipt/'])
@pytest.mark.django_db
def test_log_required_views_unlogged(url, client):
    client.get(url)
    assertTemplateUsed(template_name='sign_in.html')


@pytest.mark.django_db
def test_log_in_incorrect_data(client):
    response = client.post(
        '/sign_in', {"email": "test@test.test", "password": "incorrect"})
    assert response.url == '/sign_in/'
