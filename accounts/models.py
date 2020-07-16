from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail  
from django.contrib.auth import get_user_model
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, full_name='', phone_number=''):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone_number='', full_name=''):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(email,
                        password=password,
                        phone_number=phone_number,
                        full_name=full_name

                    )
        u.is_admin = True
        u.is_active = True
        u.save(using=self._db)
        return u


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
    full_name = models.CharField(verbose_name='fullname', blank=True, max_length=150)
    username = models.CharField(verbose_name='username', blank=True, max_length=150)
    first_name = models.CharField(verbose_name='firstname', blank=True, max_length=150)
    last_name = models.CharField(verbose_name='lastname', blank=True, max_length=150)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])
    timestamp = models.DateTimeField(auto_now_add=True)
    is_tutor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

