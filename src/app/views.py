from django.shortcuts import render


def test_view(request):
    return render(request, "pages/main.html")


def sign_up(request):
    return render(request, "pages/sign_up.html")

def sign_in(request):
    return render(request, "pages/sign_in.html")