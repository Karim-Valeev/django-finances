from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from app.decorators import not_authorized
from app.forms import RegistrationForm, AuthForm, NoteForm, ReceiptForm, CodeForm
from app.services import *
from app.tasks import send_code


def test_view(request):
    if request.user.is_authenticated:
        data = get_main_page_data(request.user)
        return render(request, "pages/main.html", data)
    else:
        return render(request, "pages/unauthorized_main.html")


@not_authorized
def start_sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            user = register_user(email, name, password)
            send_code.delay(email)
            return redirect("end_sign_up")

        return render(request, "pages/start-sign-up.html", {"form": form})

    return render(request, "pages/start-sign-up.html")


@not_authorized
def end_sign_up(request):
    form = CodeForm()
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            unverified_user = find_unverified_user(code)
            if not unverified_user.is_email_verified:
                user = verify_user_email(unverified_user)
                login(request, user)
                return redirect("main")
            else:
                return redirect('sign_in')
        else:
            form.add_error("code", "Неправильный формат кода")
    return render(request, "pages/end-sign-up.html", {'form': form})


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
                if user.is_email_verified:
                    login(request, user)
                    return redirect("main")
                else:
                    form.add_error("email", "Вы не подтвердили свою почту")

    return render(request, "pages/sign_in.html", {"form": form})


@login_required
def logout_page(request):
    logout(request)
    return redirect("main")


@login_required
def receipt_view(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            process_receipt(request.FILES['receipt'], request.user)
    return redirect("main")


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


class Analysis(TemplateView, LoginRequiredMixin):
    template_name = "pages/analysis.html"

    def get_context_data(self, **kwargs):
        context = super(Analysis, self).get_context_data(**kwargs)

        context['graph_all'] = make_all_chart(self.request.user)
        context['graph_monthly'] = make_monthly_chart(self.request.user)

        return context
