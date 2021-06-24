from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.decorators import not_authorized
from app.forms import RegistrationForm, AuthForm
from app.services import register_user


def test_view(request):
    if request.user.is_authenticated:
        return render(request, "pages/main.html")
    else:
        return render(request, "pages/unauthorized_main.html")


@not_authorized
def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            user = register_user(email, name, password)
            login(request, user)
            return redirect("main")

        return (request, "pages/sign_up.html", {"form": form})

    return render(request, "pages/sign_up.html")


@not_authorized
def sign_in(request):
    form = AuthForm()
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is None:
                form.add_error("email", "Неправильный логин или пароль")
            else:
                login(request, user)
                return redirect("main")

    return render(request, "pages/sign_in.html", {"form": form})


@login_required
def logout_page(request):
    logout(request)
    return redirect("main")
