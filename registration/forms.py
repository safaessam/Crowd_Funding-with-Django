from django.contrib.auth import authenticate
from django import forms
from projects.models import Picture, Project
from registration.models import MyUser


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "mobile_phone",
            "profile_picture",
        ]
        widgets = {
            "password": forms.PasswordInput(),
            "profile_picture": forms.FileInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "details",
            "category",
            "target_amount",
            "start_time",
            "end_time",
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].widget.attrs["readonly"] = True

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["image"]
        widgets = {"image": forms.ClearableFileInput()}


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        if len(code) != 6:
            raise forms.ValidationError("Invalid code.")
        return cleaned_data
