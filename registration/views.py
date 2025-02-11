from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from projects.models import Category, Project
from .forms import (
    EmailVerificationForm,
    RegistrationForm,
    SignInForm,
)
from registration.models import MyUser, UserEmailVerification
from django.db.models import Avg

def category_projects(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = Project.objects.filter(category=category, end_time__gte=timezone.now())

    return render(
        request,
        "projects/category_projects.html",
        {"category": category, "projects": projects},
    )


def home(request):
    signed_in = request.session.get("user_email")
    if signed_in:
        latest_projects = Project.objects.filter(end_time__gte=timezone.now()).order_by(
            "-start_time"
        )[:5]
        
        featured_projects = Project.objects.filter(
            is_featured=True, end_time__gte=timezone.now()
        ).order_by("-start_time")[:5]
        
        highest_rated_projects = Project.objects.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')[:5]
        
        categories = Category.objects.all()

        return render(
            request,
            "registration/home.html",
            {
                "latest_projects": latest_projects,
                "featured_projects": featured_projects,
                "highest_rated_projects": highest_rated_projects,
                "categories": categories,
            },
        )
    else:
        return redirect("signin")


def Registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if MyUser.objects.filter(email=email).exists():
                form.add_error("email", "Email already exists.")
                return render(
                    request, "registration/registration_form.html", {"form": form}
                )

            new_user = MyUser.objects.create(
                first_name=form.cleaned_data["first_name"].title(),
                last_name=form.cleaned_data["last_name"].title(),
                email=email,
                password=form.cleaned_data["password"],
                mobile_phone=form.cleaned_data["mobile_phone"],
                profile_picture=form.cleaned_data["profile_picture"],
                is_active=True,
            )
            new_verification = UserEmailVerification(email=new_user.email)
            new_verification.generateCode()
            new_verification.sendCode()
            new_user.save()
            # Send email verification
            request.session["user_email"] = new_user.email
            request.session["first_name"] = new_user.first_name
            return redirect("verify_email")
    else:
        form = RegistrationForm()
    return render(request, "registration/registration_form.html", {"form": form})


def signin(request):
    if request.method == "GET":
        form = SignInForm()
        return render(request, "registration/signin_form.html", {"form": form})

    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            try:
                user = MyUser.objects.get(email=email)
                if user.isEmailVerified:
                    if user.password == password:
                        request.session["user_email"] = email
                        request.session["first_name"] = user.first_name
                        return redirect("home")
                    else:
                        form.add_error(None, "Invalid email or password")
                else:
                    form.add_error(None, "Please verify your email first.")
            except MyUser.DoesNotExist:
                form.add_error(None, "User does not exist")
        return render(request, "registration/signin_form.html", {"form": form})


def signout(request):
    request.session.clear()
    return redirect("signin")


class VerifyEmail(View):
    def get(self, request):
        logged_in = request.session.get("user_email")
        if not logged_in:
            return redirect("signin")
        form = EmailVerificationForm()

        return render(request, "registration/verify_email.html", {"form": form})

    def post(self, request):
        form = EmailVerificationForm(request.POST)
        email = request.session.get("user_email")
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
