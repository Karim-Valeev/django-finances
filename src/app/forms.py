from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    name = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data


class AuthForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class Note(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    amount = forms.IntegerField(required=True)
    income = forms.BooleanField(required=True)
    input_date = forms.DateTimeField(required=True)
    constant = forms.BooleanField(required=True)
    description = forms.CharField(required=True, max_length=100)
    over_date = forms.DateField()
    note_type = forms.CharField(required=True, max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['amount'] <= 0:
            self.add_error("amount", "Сумма должна быть больше 0")
        return cleaned_data