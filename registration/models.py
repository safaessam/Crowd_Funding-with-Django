from datetime import datetime, timedelta
import random
from django.db import models
from django.core.mail import send_mail

# Create your models here.
class MyUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    mobile_phone = models.CharField(max_length=11)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    isEmailVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class UserEmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, default=000000)
    expireTime = models.DateTimeField()

    def __str__(self):
        return f"{self.email} | {self.code} | expires: {self.expireTime}"

    def sendCode(self):
        send_mail(
            subject="Welcome to the platform",
            message=f"Thank you for signing up to our platform\nYour verification code is: {self.code}",
            from_email="noreply@myfundingplatform.com",
            recipient_list=[self.email],
            fail_silently=False,
        )

    def generateCode(self):
        self.code = random.randint(100000, 999999)
        self.expireTime = datetime.now() + timedelta(days=1)
        self.save()
