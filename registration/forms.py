from django.contrib.auth import authenticate

from django import forms
from django import forms
from .models import Project, Picture

class MyUserForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    mobile_phone = forms.CharField(max_length=11)
    profile_picture = forms.ImageField(required=False)
  
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



class SignInForm(forms.Form):
    email = forms.EmailField( )
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")

        return cleaned_data

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'target_amount', 'start_time', 'end_time']

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']
        widgets = {'image': forms.ClearableFileInput()}
        