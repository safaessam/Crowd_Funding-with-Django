from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'mobile_phone', 'profile_picture', 'password') # Add editable fields
                # Other optional
