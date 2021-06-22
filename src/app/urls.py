from django.urls import path, re_path

from app.views import test_view

urlpatterns=[
    path("", test_view),
]