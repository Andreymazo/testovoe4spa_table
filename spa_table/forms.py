from django.contrib.auth.forms import UserCreationForm, UsernameField, PasswordResetForm, AuthenticationForm

from spa_table.models import CustomUser
from django import forms


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''


class SigninForm(StyleFormMixin, AuthenticationForm):
    pass


class SignupForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {"username": UsernameField}


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    # file_wave = forms.FileField()


class RegisterForm(UserCreationForm):
    # geeks_field = forms.FileField()
    # file_wave = forms.FileField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'file_wav']


class CustomUserForm(forms.Form):
    file_wav = forms.FileField()
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'file_wav']
