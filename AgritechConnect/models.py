from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model


class Farmer(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Enter phone number in the format: +123456789. Up to 15 digits allowed."
    )
    regNo = models.CharField(max_length=10, unique=True, blank=True)

    # Override the groups and user_permissions fields to avoid related name conflicts
    groups = models.ManyToManyField(
        Group, related_name='farmer_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='farmer_permissions_set', blank=True)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required during user creation

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"{self.first_name}{self.last_name}".lower()

        if not self.regNo:
            last_fmr_number = Farmer.objects.count()
            new_fmr_number = last_fmr_number + 1
            self.regNo = f"FMR{new_fmr_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.regNo

class City(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):  # show the actual city name on the dashboard
        return self.name

    class Meta:  # show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
        


class ForumPost(models.Model):
    author = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(ForumPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(ForumPost, related_name='tags')

    def __str__(self):
        return self.name
    
class BestPracticeVideo(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title


