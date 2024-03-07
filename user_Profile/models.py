from django.db import models
from projects.models import Project
from registration.models import MyUser


class UserProfile(MyUser): # Abstract user
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    # projects = models.ForeignKey(Project, on_delete = models.PROTECT)
    projects = models.ManyToManyField(Project)
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# class Projects (UserProfile):
#     title = models.CharField(max_length=50)
#     details = models.CharField(max_length=150, blank=True)
#     category = models.ForeignKey('Category', on_delete=models.PROTECT)
#     pictuers = models.ImageField(upload_to='project/')
#     total_target = models.IntegerField()
#     tags = models.ManyToManyField("Tags")
#     start_date = models.DateField(auto_now_add=True)
#     end_date = models.DateField(blank=True, null=True)

# class Donation (models.Model):
#     user = models.ForeignKey(UserProfile ,on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
#     message = models.CharField(max_length=100, blank=True)
