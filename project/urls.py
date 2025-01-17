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
from projects.views import create_project, donate, project_detail, rate_project, search_projects
from registration.views import Registration, VerifyEmail, category_projects, home, signin, signout
from user_Profile.views import user_profile

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', home, name='home' ),
    path('registration/', Registration, name='registration' ),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('project_detail/<int:project_id>/', project_detail, name='project_detail'),   
    path('project/<int:project_id>/donate/', donate, name='donate'),
    path('create_project/', create_project, name='create_project'),
    path('category_projects/<int:category_id>/', category_projects, name='category_projects'),
    path('verify_email/', VerifyEmail.as_view(), name='verify_email'),
    path('search/', search_projects, name='search_projects'),
    path('rate_project/<int:project_id>/', rate_project, name='rate_project'),
    path('profile/', user_profile , name="user_profile"),
    
]