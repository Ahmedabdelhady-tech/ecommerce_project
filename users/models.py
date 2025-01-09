from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, phone_number=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=10, blank=True, null=True)  
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def get_full_name(self):
        """
        Returns the first name and last name of the user.
        """
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def __str__(self):
        """
        Returns the email of the user as the string representation.
        """
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
