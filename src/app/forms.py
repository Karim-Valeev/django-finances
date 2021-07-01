from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=320, required=True)
    password = forms.CharField(max_length=50, required=True)
    name = forms.CharField(max_length=150, required=True)
    password2 = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data


class AuthForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class NoteForm(forms.Form):
    amount = forms.IntegerField(required=True)
    date = forms.DateTimeField(required=True)
    description = forms.CharField(required=True, max_length=100)
    note_type = forms.CharField(required=True, max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['amount'] <= 0:
            self.add_error("amount", "Сумма должна быть больше 0")
        return cleaned_data


class ReceiptForm(forms.Form):
    receipt = forms.FileField()


class CodeForm(forms.Form):
    code = forms.RegexField(required=True, regex=r'^\d{6}$')
