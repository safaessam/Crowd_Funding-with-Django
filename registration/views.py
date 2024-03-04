from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Donation, Picture, Project
# from django.contrib.auth.decorators import login_required
from registration import models
from .forms import ProjectForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from registration.forms import MyUserForm, SignInForm
from registration.models import MyUser


def home(request):
    if request.user.is_authenticated:
        return render(request, 'registration/home.html')
    else:
        return redirect('signin')


class Registration(View):
    def get(self, request):
        form = MyUserForm()
        return render(request, 'registration/registration_form.html', {'form': form})

    def post(self, request):
        form = MyUserForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = MyUser(
                first_name=form.cleaned_data['first_name'].title(),
                last_name=form.cleaned_data['last_name'].title(),
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                profile_picture=request.FILES.get('profile_picture'),
                is_active=False
            )
            new_user.save()
            return redirect('signin')

        return render(request, 'registration/registration_form.html', {'form': form})


class SignIn(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = SignInForm()
        return render(request, 'registration/signin_form.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')

        form = SignInForm()
        return render(request, 'registration/home.html', {'form': form})


def signout(request):
    request.session.clear()
    logout(request)
    return redirect('signin')


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    average_rating = project.reviews.aggregate(models.Avg('rating'))['rating__avg']
    return render(request, 'registration/project_detail.html', {'project': project, 'average_rating': average_rating})

def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        donation = Donation.objects.create(project=project, user=request.user, amount=amount)
        return redirect('registration/project_detail.html', project_id=project.id)
    return render(request, 'donate.html', {'project': project})

def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        picture_form = PictureForm(request.POST, request.FILES)
        if project_form.is_valid() and picture_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            for f in request.FILES.getlist('image'):
                picture = Picture(project=project, image=f)
                picture.save()
            return redirect('registration/project_detail.html', project_id=project.id)
    else:
        project_form = ProjectForm()
        picture_form = PictureForm()
    return render(request, 'registration/create_project.html', {'project_form': project_form, 'picture_form': picture_form})