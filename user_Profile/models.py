from django.db import models

from registration.models import MyUser

# Create your models here.

class UserProfile (models.Model):
    first_name =  models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=False)
    password =  models.CharField(max_length=25)
    profile_picture =  models.ImageField(upload_to='profile/',blank=True)
    

# class UserProfile(MyUser):
#     birthdate = models.DateField(null=True, blank=True)
#     facebook_profile = models.URLField(null=True, blank=True)
#     country = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         verbose_name = 'User Profile'
#         verbose_name_plural = 'User Profiles'

class Projects (UserProfile):
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=150, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    pictuers = models.ImageField(upload_to='project/')
    total_target = models.IntegerField()
    tags = models.ManyToManyField("Tags")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

class Donation (models.Model):
    user = models.ForeignKey(UserProfile ,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100, blank=True)
