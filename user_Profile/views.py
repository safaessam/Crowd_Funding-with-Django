from django.shortcuts import redirect, render
from registration.models import MyUser


def user_profile(request):
    user_email = request.session.get("user_email")
    if user_email:
        try:
            user = MyUser.objects.get(email=user_email)
        except MyUser.DoesNotExist:
            user = None
        
        context = {
            'user_profile': user
        }
        return render(request, 'profiles/profile_detail.html', context)
    else:
        return redirect("signin")
