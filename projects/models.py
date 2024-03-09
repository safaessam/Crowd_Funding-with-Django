from django.db import models
from django.utils import timezone
from registration.models import MyUser

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    picture = models.ImageField(upload_to='static/project_images')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField('Tag')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    # Existing fields
    def __str__(self):
            return self.title
        
    def average_rating(self):
            total_rating = sum([rating.value for rating in self.ratings.all()])
            if total_rating:
                return total_rating / self.ratings.count()
            return 0

    def cancel_project(self):
            total_donations = sum([donation.amount for donation in self.donations.all()])
            return total_donations < 0.25 * self.target_amount

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.project.title}"


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.project.title}"


class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} donated {self.amount}"


class FeaturedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

class Review(models.Model):
    comment = models.CharField(max_length=255)
    rate = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(MyUser, related_name='user_review', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='project_review', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} | {self.project} | 'comment' --> {self.comment}"