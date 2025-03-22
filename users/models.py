from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from services.models import Service

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username должен быть указан')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Номер телефона")

    first_name = models.CharField(max_length=120, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=120, verbose_name="Фамилия", null=True, blank=True)
    surname = models.CharField(max_length=120, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False, verbose_name="Является мастером")
    services = models.ManyToManyField(Service, blank=True, related_name="masters", verbose_name="Предоставляемые услуги")

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.username} - {self.phone_number}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    