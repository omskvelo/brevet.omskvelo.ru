from django.db import models
from django.contrib.auth.models import AbstractUser


from phonenumber_field.modelfields import PhoneNumberField

from brevet_database.models import Randonneur
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    randonneur = models.ForeignKey(Randonneur, on_delete=models.PROTECT, default=239)
    phone_number = PhoneNumberField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    ordering = ('email',)

    def __str__(self):
        return self.email 

    class Meta:
        db_table = 'auth_user'