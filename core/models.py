from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, F

from department.models import Division, GRC


class UserManager(BaseUserManager):
    def admin_create_user(self, username, division, soeId, password=None, grc=None, department=None):
        """
        Creates and saves a User with the given username, date of birth, department, soeId and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        if grc and department:
            grc_obj = GRC.objects.filter(grc_name=grc, user_department__department_name=department).first()
            division_obj = Division.objects.filter(division_name=division, grc=grc_obj).first()
        else:
            division_obj = Division.objects.filter(id=division).first()

        if not division_obj:
            raise ValueError('Division does not exists')

        user = self.model(
            username=username,
            division=division_obj,
            soeId=soeId,
        )
        if password:
            user.set_password(password)
        else:
            user.set_password(soeId)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, division=None, soeId='999', email=None,
                         password=None):
        """
        Creates and saves a superuser with the given username, department, soeId and password.
        """
        division_obj = Division.objects.filter(id=division).first()

        user = self.model(
            username=username,
            division=division_obj,
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

    def get_total_users_by_user_department(self):
        users = User.objects.filter(
            is_staff=False, is_active=True
        ).exclude(
            division__grc__user_department__department_name='NA'
        ).values('division__grc__user_department__department_name').annotate(
            department_name=F('division__grc__user_department__department_name'),
            total=Count('division__grc__user_department__department_name'),
            # active=Count(Case(When(last_login__isnull=False, then=1), output_field=IntegerField()))
        ).values('department_name', 'total')

        return users


class User(AbstractUser):
    soeId = models.CharField(max_length=50, blank=True, unique=True)
    mac_id = models.TextField(default="")
    division = models.ForeignKey(Division, on_delete=models.PROTECT, related_name='user', blank=True, null=True)
    is_completed_tutorial = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username
