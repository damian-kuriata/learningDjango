from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from catalog.models import UploadedImage

class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ["title", "description", "image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"multiple": False}),
            "description": forms.Textarea(attrs={"rows": "4", "cols":"41",
                                                 "placeholder": "My beautiful image"})
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
    password1 = forms.CharField(max_length=150, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        # Check whether both passwords don't match
        if cleaned_data["password1"] != cleaned_data["password2"]:
            raise ValidationError("Both passwords must match", code="invalid")
        # Check whether username is already in use
        try:
            username = cleaned_data["username"]
            User.objects.get(username__iexact=username)
            msg = "User named %(user)s already exists"
            raise ValidationError(msg, params={"user": username},
                                  code="invalid")
        except User.DoesNotExist:
            pass
        # Check whether email is already in use
        try:
            email = cleaned_data["email"]
            User.objects.get(email__iexact=email)
            msg = f"Email {email} already in use"
            self.add_error("email", msg)
        except User.DoesNotExist:
            pass
