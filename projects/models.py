from django.db import models

from registration.models import MyUser

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pictures = models.ManyToManyField('Picture')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField('Tag')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment')
    ratings = models.ManyToManyField('Rating')
    is_cancelled = models.BooleanField(default=False)

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
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"

class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"

class Picture(models.Model):
    image = models.ImageField(upload_to='project_images')

    def __str__(self):
        return self.image.name