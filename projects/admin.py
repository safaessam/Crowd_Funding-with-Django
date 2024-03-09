from django.contrib import admin
from projects.models import (
    Category,
    Comment,
    Donation,
    FeaturedProject,
    Project,
    Rating,
    Review,
    Tag,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Donation)
admin.site.register(FeaturedProject)
admin.site.register(Review)
