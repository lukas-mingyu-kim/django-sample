from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class AtmUserManager(BaseUserManager):

    def create_user(self, card_num, password=None):
        if not card_num:
            raise ValueError('User must have an card num')
        user = self.model(card_num=card_num)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, card_num, password=None):
        user = self.create_user(card_num, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AtmUser(AbstractBaseUser, PermissionsMixin):
    card_num = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AtmUserManager()

    USERNAME_FIELD = 'card_num'


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    account_num = models.CharField(max_length=20, unique=True)
    balance = models.IntegerField(default=0)
