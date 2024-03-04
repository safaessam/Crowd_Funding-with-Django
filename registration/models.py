from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=11)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# class Project(models.Model):
#     title = models.CharField(max_length=100)
#     details = models.TextField()
#     category = models.CharField(max_length=100)
#     target_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


# class Picture(models.Model):
#     project = models.ForeignKey(
#         Project, on_delete=models.CASCADE, related_name="pictures"
#     )
#     image = models.ImageField(upload_to="project_pictures")


# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#     projects = models.ManyToManyField(Project, related_name="tags")

#     def __str__(self):
#         return self.name


# class Donation(models.Model):
#     project = models.ForeignKey(
#         Project, on_delete=models.CASCADE, related_name="donations"
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} donated {self.amount}"
