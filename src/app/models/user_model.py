from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager as DjangoUserManager
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_superuser=True)
        user.set_password(password)
        user.save()
        return user




class WalletUser(AbstractBaseUser, PermissionsMixin):
    object = UserManager()

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=False, default="Wallet")
    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        db_table = "WalletUser"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
