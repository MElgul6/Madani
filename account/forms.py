from dataclasses import field
from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, password_validation
from account.models import User
from account.tasks import send_confirmation_mail



class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={
        'class':'form-controll',
        'placeholder':'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-controll',
        'placeholder':'Password'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control',
                'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control',
                'placeholder': 'Confirm Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
            'email',
            'phone',
            'is_active',
            'password1',
            'password2'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone'
            }),
            'is_active': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'is_active'
            }),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
            'email',
            'phone',
            'password'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone'
            }),
        }


class CustomChangePasswordForm(PasswordChangeForm):
  
        oldpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Old Password'
}))
        newpassword1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'New password'
                                          }),
        
    )
        newpassword2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Confirm Password'}),
        help_text=("Enter the same password as before, for verification."),
    )

        def clean(self):
            newpassword1 = self.cleaned_data.get('newpassword1')
            newpassword2 = self.cleaned_data.get('newpassword2')
            if newpassword1 != newpassword2:
                raise forms.ValidationError('password and confirm password is not same')
            return super().clean()
