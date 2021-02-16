from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Case, When, IntegerField

from department.models import Division, UserDepartment, GRC


class UserManager(BaseUserManager):
    def admin_create_user(self, username, grc, user_department, division, soeId, password=None):
        """
        Creates and saves a User with the given username, date of birth, department, soeId and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user_department_obj = UserDepartment.objects.filter(department_name=user_department).first()
        if not user_department_obj:
            raise ValueError('Users department does not exists')
        grc_obj = GRC.objects.filter(user_department=user_department_obj, grc_name=grc).first()
        if not grc_obj:
            raise ValueError('GRC does not exists')
        division_obj = Division.objects.filter(grc=grc_obj, division_name=division).first()
        if not division_obj:
            raise ValueError('Division does not exists')

        user = self.model(
            username=username,
            # grc=grc,
            # regional_office=regional_office,
            # department=department,
            division=division_obj,
            soeId=soeId,
            # profile_pic=profile_pic
        )
        if password:
            user.set_password(password)
        else:
            user.set_password(soeId)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, grc=None, division=None, user_department=None, soeId='999', email=None,
                         password=None):
        """
        Creates and saves a superuser with the given username, department, soeId and password.
        """
        division_obj = None

        user_department_obj = UserDepartment.objects.filter(department_name=user_department).first()
        if user_department_obj:
            grc_obj = GRC.objects.filter(user_department=user_department_obj, grc_name=grc).first()
            if grc_obj:
                division_obj = Division.objects.filter(grc=grc_obj, division_name=division).first()

        user = self.model(
            username=username,
            division=division_obj,
            # grc=grc,
            # regional_office=regional_office,
            # department=department,
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
    # department = models.CharField(max_length=100, blank=True)
    mac_id = models.TextField(default="")
    division = models.ForeignKey(Division, on_delete=models.PROTECT, related_name='user', blank=True, null=True)
    # grc = models.CharField(max_length=256, blank=True)
    # regional_office = models.CharField(max_length=256, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
