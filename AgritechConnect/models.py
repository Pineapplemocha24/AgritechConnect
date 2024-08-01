from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

# Farmer
class Farmer(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Enter phone number in the format: +123456789. Up to 15 digits allowed."
    )
    regNo = models.CharField(max_length=10, unique=True, blank=True)

    # Define groups and user_permissions with related_name to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='farmer_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='farmer_permissions_set', blank=True)

    def save(self, *args, **kwargs):
        if not self.regNo:
            # Get the number of existing farmers and add 1 for the new one
            last_fmr_number = Farmer.objects.count()
            new_fmr_number = last_fmr_number + 1
            self.regNo = f"FMR{new_fmr_number:04d}"  # Format as "FMR0001", "FMR0002", etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

