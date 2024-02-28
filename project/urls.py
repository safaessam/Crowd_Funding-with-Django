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
from django import views
from django.contrib import admin
from django.urls import path
from registration.views import Registration, SignIn, create_project, donate, home, project_detail,signout

urlpatterns = [ 

    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('registration/', Registration.as_view(), name='registration'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signout/', signout, name='signout'),
    path('project_detail/<int:project_id>/', project_detail, name='project_detail'),   
    path('project/<int:project_id>/donate/', donate, name='donate'),
    path('create_project/', create_project, name='create_project'),


]