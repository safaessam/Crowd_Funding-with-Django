from sqlite3 import IntegrityError
from django.shortcuts import redirect, render
from django.views import View
from registration.forms import MyUserForm
from registration.models import MyUser

# Create your views here.
def home(request):
    return render(request, 'registration/home.html')

class Registration(View):
    def get(self, request):
        form = MyUserForm()
        return render(request, 'registration/registration_form.html', {'form': form})

    def post(self, request):
        form = MyUserForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].title()
            last_name = form.cleaned_data['last_name'].title()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mobile_phone = form.cleaned_data['mobile_phone']
            profile_picture = request.FILES.get('profile_picture')

            new_user = MyUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                mobile_phone=mobile_phone,
                profile_picture=profile_picture,
                is_active=False
            )
            new_user.save()
            
            return redirect('home')
        return render(request, 'registration/registration_form.html', {'form': form})