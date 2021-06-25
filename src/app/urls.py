from django.urls import path, re_path

from app.views import test_view, sign_up, sign_in, logout_page, income_view, consumption_view, receipt_view

urlpatterns = [
    path("", test_view, name="main"),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_in/", sign_in, name="sign_in"),
    path("logout/", logout_page, name="logout"),
    path("income/", income_view, name="income"),
    path("consumption/", consumption_view, name="consumption"),
    path("receipt/", receipt_view, name="receipt")
]
