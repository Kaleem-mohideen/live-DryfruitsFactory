from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phone_field import PhoneField
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="Email", null=True,unique=True, max_length=100)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')





