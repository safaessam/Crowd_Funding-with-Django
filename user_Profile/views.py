from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from user_Profile.models import UserProfile

@login_required
def profile_detail(request):
    user = get_object_or_404(UserProfile, pk=request.user.pk)
    projects = user.projects.all()  # Assuming you have a 'projects' relation
    donations = user.donations.all()  # Assuming you have a 'donations' relation
    context = {'user': user, 'projects': projects, 'donations': donations}
    return render(request, 'profiles/profile_detail.html', context)
