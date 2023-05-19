import uuid as uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_tables2 import tables

NULLABLE = {'blank': True, 'null': True}
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username or username is None:
            raise ValidationError("User must have username")
        if not email or email is None:
            raise ValidationError("User must have email address")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# https://ilovedjango.com/django/authentication/custom-user-model-in-django/
class CustomUser(AbstractBaseUser):  # , PermissionsMixin):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50,
                                unique=True)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_by = models.ForeignKey('CustomUser',
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name="custom_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id}: {self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Values_table(models.Model):
    data = models.TimeField(auto_now_add=True, verbose_name='Дата')
    name = models.CharField(max_length=100, verbose_name='Название')
    quantity = models.IntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)],
                                   verbose_name='Количество')
    distance = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(0)],
                                   verbose_name='Расстояние')


class Values_tableTable(tables.Table):
    class Meta:
        model = Values_table
#

class Question(models.Model):
    body = models.CharField(max_length=300, verbose_name='Название вопроса')
    answer = models.CharField(max_length=150, verbose_name='Ответ')
    question_value = models.IntegerField(validators=[MaxValueValidator(1500), MinValueValidator(0)],
                                         verbose_name='Количество баллов за вопрос', **NULLABLE)
    created = models.TimeField(auto_now_add=True)


class QuestionTable(tables.Table):
    class Meta:
        model = Question
