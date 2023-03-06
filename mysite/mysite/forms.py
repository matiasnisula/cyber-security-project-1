from django import forms

class SecurityRiskSignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=130)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())