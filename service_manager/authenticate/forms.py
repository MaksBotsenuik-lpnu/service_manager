from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate

from authenticate.models.user import User
from service.models.device import Device


class UserRegisterForm(UserCreationForm):
    """
    Form that allows to register as jobseeker or employer.
    """
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = False  # Always set to False by default
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone = self.cleaned_data["phone"]
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    """
    Form for user authentication which allows users
    to log in using their email and password.
    """
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,  # Use email as username
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password. Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    """
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field read-only
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control bg-light'


