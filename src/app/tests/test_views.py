from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from app.models import WalletUser
from app.models import Note
from app.views import sign_in
# from barbook_app.views import CreateCocktail


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
