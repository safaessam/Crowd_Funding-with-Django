"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from registration.views import Registration, home
from user_Profile.views import donations, projects, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_profile , name="user profile"),
    path('projects', projects , name='projects'),
    path('donations', donations , name='donations'),
    path('registration/', Registration.as_view(), name='registration' ),
    path('home/', home, name='home' ),

]