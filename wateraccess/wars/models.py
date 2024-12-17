from asyncio.log import logger
import logging
from django.utils.timezone import now
from django.db import models
from django.db.models import Max
from django.contrib.auth.hashers import Argon2PasswordHasher
from argon2 import PasswordHasher

# Create your models here.

# Argon2 Password Hasher
password_hasher = PasswordHasher()

# User Model
class warsUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    names = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    nationalId = models.CharField(max_length=16)
    dob = models.DateField(default='2000-01-01')
    gender= models.CharField(max_length=10, default='Other')
    nationality= models.CharField(max_length=100, default='Rwandan')
    emergencyContact= models.CharField(max_length=15 , null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.names

# Location Model
class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(warsUser, on_delete=models.CASCADE, related_name='location')
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    cell = models.CharField(max_length=100, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Location for {self.user.names}"

# Password Model
class Password(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(warsUser, on_delete=models.CASCADE, related_name='password')
    password_hash = models.CharField(max_length=255)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_expiration_time = models.DateTimeField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expiration = models.DateTimeField(null=True, blank=True)
    last_changed_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        hasher = Argon2PasswordHasher()
        self.password_hash = hasher.encode(raw_password, hasher.salt())
        self.save()

    def __str__(self):
        return f"Password details for {self.user.names}"

# Profile Model
class userProfile(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Responsible', 'Responsible'),
        ('Customer', 'Customer'),
        ('Technician', 'Technician'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    NATIONALITY_CHOICES = [
        ('Rwandan', 'Rwandan'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(warsUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, default='Rwandan')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')

    def __str__(self):
        return f"{self.user.names} - {self.role}"

class Tap(models.Model):
    customer_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tap_id = models.CharField(max_length=20, unique=True)
    date_added = models.DateTimeField(default=now)  # Use timezone-aware now

    logger = logging.getLogger(__name__)

def save(self, *args, **kwargs):
    if not self.tap_id:
        year = now().year
        attempts = 0  # Add a counter for attempts
        while True:
            attempts += 1
            logger.info(f"Attempt {attempts}: Generating tap_id for year {year}.")
            
            last_tap = Tap.objects.filter(tap_id__startswith=str(year)).aggregate(max_id=Max('tap_id'))['max_id']
            if last_tap:
                next_number = int(last_tap[4:]) + 1
            else:
                next_number = 1

            generated_id = f"WASAC{year}{str(next_number).zfill(4)}"
            if not Tap.objects.filter(tap_id=generated_id).exists():
                self.tap_id = generated_id
                break  # Exit the loop if unique ID found
            if attempts > 10:  # Add a safeguard to prevent infinite loop
                raise Exception("Failed to generate a unique tap_id after 10 attempts.")
    super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.tap_id} - {self.customer_name} ({self.location})"

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    reporter_name = models.CharField(max_length=255, default="Anonymous")  # Default for existing rows
    reporter_email = models.EmailField(default="no-2reply@example.com")      # Default for existing rows
    tap_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='cases/files/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')  # Example: Pending, Resolved
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




# ContactMessage model

class ContactMessage(models.Model):
    names = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    file = models.FileField(upload_to='uploads/contacts/', blank=True, null=True)  # Adjust the upload path as needed
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.names}{self.phone}{self.email}{self.message}{self.file} ({self.email})"






# Models for the Wars app user registration data
class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sectors')

    def __str__(self):
        return self.name


class Cell(models.Model):
    name = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='cells')

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='villages')

    def __str__(self):
        return self.name