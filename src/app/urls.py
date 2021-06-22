from django.urls import path, re_path

from app.views import test_view, sign_up, sign_in

urlpatterns = [
    path("", test_view),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_in/", sign_in, name="sign_in")
]
