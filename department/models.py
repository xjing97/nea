from django.db import models
from django.db.models import Count


class UserDepartmentManager(models.Manager):
    def get_total_users_by_user_department(self):
        users = UserDepartment.objects.exclude(
            department_name='NA', grc__division__user__is_staff=True,
        ).values('department_name').annotate(
            total=Count('grc__division__user__username')
        ).values('department_name', 'total')

        return users


class UserDepartment(models.Model):
    department_name = models.CharField(max_length=256, default="", unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = UserDepartmentManager()

    def __str__(self):
        return self.department_name


class GRC(models.Model):
    user_department = models.ForeignKey(UserDepartment, on_delete=models.PROTECT, related_name='grc')
    grc_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_department', 'grc_name']

    def __str__(self):
        return self.grc_name


class Division(models.Model):
    grc = models.ForeignKey(GRC, on_delete=models.PROTECT, related_name='division')
    division_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['grc', 'division_name']

    def __str__(self):
        return self.division_name
