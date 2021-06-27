from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.decorators import not_authorized
from app.forms import RegistrationForm, AuthForm, NoteForm
from app.services import register_user, get_main_page_data, new_note, pay_note, delete_note


def test_view(request):
    if request.user.is_authenticated:
        data = get_main_page_data(request.user)
        return render(request, "pages/main.html", data)
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


def receipt_view(request):
    print(request.POST)


@login_required
def new_note_view(request):
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note(form, request.user)
        else:
            print(form.errors)
    return redirect('main')


@login_required
def pay_constant_note(request, pk):
    pay_note(request.user, pk)
    return redirect("main")


@login_required
def delete_note_view(request, pk):
    delete_note(request.user, pk)
    return redirect("main")
