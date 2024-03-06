from django.db import models


# Create your models here.
class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=11)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
