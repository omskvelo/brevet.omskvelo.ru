from xmlrpc.client import Boolean
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
    randonneur = models.ForeignKey(Randonneur, on_delete=models.PROTECT, default=239)
    phone_number = PhoneNumberField()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    ordering = ('email',)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.phone_number} "

    def get_username(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'auth_user'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}  {'v' if self.email_confirmed else 'x'}" 


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()