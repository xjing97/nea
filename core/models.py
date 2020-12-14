from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    soeId = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""

        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""

        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""

        return self.is_staff