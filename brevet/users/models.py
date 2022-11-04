from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

from brevet_database.models import Randonneur
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    randonneur = models.ForeignKey("brevet_database.Randonneur", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    phone_number = PhoneNumberField()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    ordering = ('email',)

    def __str__(self):
        return f"{self.last_name.capitalize()} {self.first_name.capitalize()} {self.phone_number} {self.email}"

    def get_username(self):
        return f"{self.email}"

    def get_display_name(self):
        return f"{self.last_name.capitalize()} {self.first_name.capitalize()}"

    def create_randonneur(self):
        if not self.randonneur:
            self.randonneur = Randonneur.from_user(self)
            self.randonneur.save()
            return True
        return False

    class Meta:
        db_table = 'auth_user'