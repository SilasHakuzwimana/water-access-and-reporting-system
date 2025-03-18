import logging
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.hashers import Argon2PasswordHasher
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# User Model
class warsUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    names = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    nationalId = models.CharField(max_length=16, unique=True)
    dob = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=10, default='Other')
    nationality = models.CharField(max_length=100, default='Rwandan')
    emergencyContact = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.names

# Location Model
class Location(models.Model):
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
    user = models.OneToOneField(warsUser, on_delete=models.CASCADE, related_name='password')
    password_hash = models.CharField(max_length=255)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_expiration_time = models.DateTimeField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expiration = models.DateTimeField(null=True, blank=True)
    last_changed_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        hasher = Argon2PasswordHasher()
        self.password_hash = hasher.encode(raw_password, 'salt')  # 'salt' should be generated securely
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
        ('Ugandan', 'Ugandan'),
        ('Kenyan', 'Kenyan'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(warsUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')  # Add this field
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, default='Other')  # Add this field

    def __str__(self):
        return f"{self.user.names} - {self.role}"


# Tap Model
class Tap(models.Model):
    customer_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tap_id = models.CharField(max_length=20, unique=True)
    date_added = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.tap_id:
            year = now().year
            attempts = 0
            while attempts < 10:
                attempts += 1
                last_tap = Tap.objects.filter(tap_id__startswith=str(year)).aggregate(max_id=Max('tap_id'))['max_id']
                next_number = int(last_tap[4:]) + 1 if last_tap else 1
                generated_id = f"WASAC{year}{str(next_number).zfill(4)}"

                if not Tap.objects.filter(tap_id=generated_id).exists():
                    self.tap_id = generated_id
                    break
            else:
                raise Exception("Failed to generate a unique tap_id after 10 attempts.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tap_id} - {self.customer_name} ({self.location})"

# Case Model
class Case(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    reporter_name = models.CharField(max_length=255, default="Anonymous")
    reporter_email = models.EmailField(default="no-reply@example.com")
    tap_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='cases/files/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# ContactMessage Model
class ContactMessage(models.Model):
    names = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    file = models.FileField(upload_to='uploads/contacts/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.names} ({self.email})"

# Address Hierarchy Models
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
