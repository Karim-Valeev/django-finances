from django.urls import path, re_path

from app.views import test_view, start_sign_up,end_sign_up, sign_in, logout_page, receipt_view, \
    new_note_view, pay_constant_note, delete_note_view, Analysis

urlpatterns = [
    path("", test_view, name="main"),
    path("sign_up/", start_sign_up, name="sign_up"),
    path("end_sign_up/", end_sign_up, name="end_sign_up"),
    path("sign_in/", sign_in, name="sign_in"),
    path("logout/", logout_page, name="logout"),
    path("new_note/", new_note_view, name="new_note"),
    path("receipt/", receipt_view, name="receipt"),
    path("pay/<int:pk>/", pay_constant_note, name="pay"),
    path("delet_note/<int:pk>/", delete_note_view, name="delete_note"),
    path("analysis/", Analysis.as_view(), name="analysis")
]
