from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, username, date_of_birth, department, soeId, profile_pic, password):
        """
        Creates and saves a User with the given username, date of birth, department, soeId and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            date_of_birth=date_of_birth,
            department=department,
            soeId=soeId,
            profile_pic=profile_pic
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, department, soeId, password=None):
        """
        Creates and saves a superuser with the given username, date of birth, department, soeId and password.
        """
        user = self.create_user(
            username=username,
            date_of_birth=date_of_birth,
            department=department,
            soeId=soeId,
            password=password
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='upload/profile-pic', default=None)
    soeId = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
