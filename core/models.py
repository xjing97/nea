from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Case, When, IntegerField


class UserManager(BaseUserManager):
    def admin_create_user(self, username, grc, regional_office, department, soeId, password=None):
        """
        Creates and saves a User with the given username, date of birth, department, soeId and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            grc=grc,
            regional_office=regional_office,
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

    def create_superuser(self, username, grc=None, regional_office=None, department='Admin', soeId='999', email=None, password=None):
        """
        Creates and saves a superuser with the given username, date of birth, department, soeId and password.
        """
        user = self.model(
            username=username,
            grc=grc,
            regional_office=regional_office,
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
        users['inactive'] = User.objects.filter(last_login__isnull=True, is_active=True).count()
        users['active'] = User.objects.filter(last_login__isnull=False, is_active=True).count()

        return users

    def get_total_users_by_department(self):
        users = User.objects.filter(
            is_staff=False, is_active=True
        ).values('department').annotate(
            total=Count('department'),
            active=Count(Case(When(last_login__isnull=False, then=1), output_field=IntegerField()))
        ).values('department', 'total', 'active')

        return users


class User(AbstractUser):
    # profile_pic = models.ImageField(upload_to='upload/profile-pic', default=None)
    soeId = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    mac_id = models.TextField(default="")
    grc = models.CharField(max_length=256, blank=True)
    regional_office = models.CharField(max_length=256, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
