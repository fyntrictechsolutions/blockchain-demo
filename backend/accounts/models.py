from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Company(models.Model):

    class CompanyType(models.TextChoices):
        MANUFACTURER = 'MANUFACTURER', 'Manufacturer'
        BUYER = 'BUYER', 'Buyer'

    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(
        max_length=20,
        choices=CompanyType.choices
    )
    company_email = models.EmailField(null=True, blank=True)
    company_phone_number = models.CharField(max_length=20, blank=True)
    company_address = models.TextField(blank=True)
    company_registration_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    company_is_active = models.BooleanField(default=True)

    company_created_at = models.DateTimeField(auto_now_add=True)
    company_updated_at = models.DateTimeField(auto_now=True)

    company_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_companies'
    )

    def __str__(self):
        return self.company_name