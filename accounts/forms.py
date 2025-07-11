from django import forms 
from django.contrib import messages
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "password"]

     #Checks for matching passwords
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter first name."
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter last name."
        self.fields["email"].widget.attrs["placeholder"] = "Enter email."
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"