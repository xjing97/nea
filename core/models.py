from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count


class UserManager(BaseUserManager):
    def admin_create_user(self, username, date_of_birth, department, soeId, password=None):
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
            # profile_pic=profile_pic
        )
        if password:
            user.set_password(password)
        else:
            user.set_password(soeId)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth=None, department='Admin', soeId='999', email=None, password=None):
        """
        Creates and saves a superuser with the given username, date of birth, department, soeId and password.
        """
        user = self.model(
            username=username,
            date_of_birth=date_of_birth,
            department=department,
            soeId=soeId,
            password=password,
            email=email
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_total_user_login(self):
        users = {'active': 0, 'inactive': 0}
        users['inactive'] = User.objects.filter(last_login__isnull=True).count()
        users['active'] = User.objects.filter(last_login__isnull=False).count()

        return users

    def get_total_users_by_department(self):
        users = User.objects.values('department').annotate(
            total=Count('department')
        ).values('department', 'total')
        return users


class User(AbstractUser):
    # profile_pic = models.ImageField(upload_to='upload/profile-pic', default=None)
    soeId = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    mac_id = models.TextField(default="")
    date_of_birth = models.DateField(null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
