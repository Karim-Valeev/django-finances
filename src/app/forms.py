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
