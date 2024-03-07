import random
from random import randint  # Import the 'random' module
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from projects import models
from projects.models import Category, Project, Donation, Picture
from .forms import EmailVerificationForm, MyUserForm, PictureForm, ProjectForm, SignInForm
from registration.models import MyUser, UserEmailVerification

from datetime import datetime, timedelta

def category_projects(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = Project.objects.filter(category=category, end_time__gte=timezone.now())
    
    return render(request, 'registration/category_projects.html', {'category': category, 'projects': projects})

def home(request):
    latest_projects = Project.objects.filter(end_time__gte=timezone.now()).order_by('-start_time')[:5]
    featured_projects = Project.objects.filter(is_featured=True, end_time__gte=timezone.now()).order_by('-start_time')[:5]
    categories = Category.objects.all()

    return render(request, "registration/home.html", {
        'latest_projects': latest_projects,
        'featured_projects': featured_projects,
        'categories': categories,
    })


# class Registration(View):
#     def get(self, request):
#         form = MyUserForm()
#         return render(request, "registration/registration_form.html", {"form": form})

#     def post(self, request):
#         form = MyUserForm(request.POST, request.FILES)
#         # if_val = MyUser.objects.filter(email=email)

#         # if form.is_valid():
#         # new_user = MyUser(
#         first_name = (form.cleaned_data["first_name"].title(),)
#         last_name = (form.cleaned_data["last_name"].title(),)
#         email = (form.cleaned_data["email"],)
#         password = (form.cleaned_data["password"],)
#         mobile_phone = (form.cleaned_data["mobile_phone"],)
#         profile_picture = (request.FILES.get("profile_picture"),)
#         is_active = (False,)
#         name = first_name + " " + last_name
#         # )
#         # new_user.save()
#         if_val = MyUser.objects.filter(email=email)
#         if if_val:
#             return render(request, "registration/registration_form.html", {"form": form})
#         User.objects.create_user(
#             username=name,
#             email=email,
#             password=password,
#             phone=mobile_phone,
#             profile_picture=profile_picture,
#             validate=is_active,
#         )
#         MyUser.objects.create(
#             username=name,
#             email=email,
#             password=password,
#             phone=mobile_phone,
#             profile_picture=profile_picture,
#             validate=is_active,
#         )

#         return redirect("signin")

#         # return render(request, "registration/registration_form.html", {"form": form})

def Registration(request):
    form_class = MyUserForm
    template_name = 'registration.html'

    if request.method == 'GET':
        form = form_class()
        return render(request, "registration/registration_form.html", {"form": form})

    elif request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # random_code = randint(100000, 999999)
            new_user = MyUser(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                profile_picture=form.cleaned_data['profile_picture'],
                is_active = True
            )
            new_verification = UserEmailVerification(
                email = new_user.email
            )
            new_verification.generateCode()  # Pass the generated code directly
            new_verification.sendCode()
            new_user.save()
            # Send email verification
            request.session['user_email'] = new_user.email
            return redirect('verify_email')
        return render(request, "registration/registration_form.html", {"form": form})


class SignIn(View):
    def get(self, request):
        # if request.user.is_authenticated:
        # return redirect("home")
        form = SignInForm()
        return render(request, "registration/signin_form.html", {"form": form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            # Add email verification
            if user:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid email or password")

        form = SignInForm()
        return render(request, "registration/home.html", {"form": form})


def signout(request):
    request.session.clear()
    logout(request)
    return redirect("signin")


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    average_rating = project.reviews.aggregate(models.Avg("rating"))["rating__avg"]
    return render(
        request,
        "registration/project_detail.html",
        {"project": project, "average_rating": average_rating},
    )


def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        amount = request.POST["amount"]
        donation = Donation.objects.create(
            project=project, user=request.user, amount=amount
        )
        return redirect("registration/project_detail.html", project_id=project.id)
    return render(request, "donate.html", {"project": project})

def create_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        picture_form = PictureForm(request.POST, request.FILES)
        if project_form.is_valid() and picture_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user #Built-in User
            project.save()
            for f in request.FILES.getlist("images"):
                picture = Picture(project=project, image=f)
                picture.save()
            return redirect("registration/project_detail.html", project_id=project.id)
    else:
        project_form = ProjectForm()
        picture_form = PictureForm()
        return render(
            request,
            "registration/create_project.html",
            {"project_form": project_form, "picture_form": picture_form},
        )

class VerifyEmail(View):
    def get(self, request):
        # if not loggedIn, redirect
        email = request.session.get('user_email')
        if not email:
            return redirect("signin")
        form = EmailVerificationForm()
        
        return render(request, "registration/verify_email.html", {"form": form})

    def post(self, request):
        form = EmailVerificationForm(request.POST)
        email = request.session.get('user_email')
        if not email:
            return redirect("signin")
        if form.is_valid():
            code = form.cleaned_data["code"]
            user = MyUser.objects.get(email=email)
            userEmailVerification = UserEmailVerification.objects.get(email=email)
            
            expireTime = userEmailVerification.expireTime
            if timezone.now() > expireTime:
                form.add_error(None, "Code expired, a new code was sent to your email!")
                userEmailVerification.generateCode()
                userEmailVerification.sendCode()
            if code == userEmailVerification.code:
                user.isEmailVerified = True
                user.save()
                return redirect("home")
            else:
                form.add_error(None, "Invalid code")
        return render(request, "registration/verify_email.html", {"form": form})