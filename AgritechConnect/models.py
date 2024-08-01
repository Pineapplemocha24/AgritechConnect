from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator

class Farmer(AbstractUser):
    # You don't need to redefine `password`, `groups`, or `user_permissions`
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        help_text="Enter phone number in the format: +123456789. Up to 15 digits allowed."
    )
    regNo = models.CharField(max_length=10, unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def save(self, *args, **kwargs):
        if not self.regNo:
            last_fmr_number = Farmer.objects.count()
            new_fmr_number = last_fmr_number + 1
            self.regNo = f"FMR{new_fmr_number:04d}"
        print(f"Saving Farmer: {self.email}, {self.first_name}, {self.last_name}")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
