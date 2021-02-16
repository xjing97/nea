from django.db import models


class UserDepartment(models.Model):
    department_name = models.CharField(max_length=256, default="", unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class GRC(models.Model):
    user_department = models.ForeignKey(UserDepartment, on_delete=models.PROTECT, related_name='grc')
    grc_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_department', 'grc_name']


class Division(models.Model):
    grc = models.ForeignKey(GRC, on_delete=models.PROTECT, related_name='division')
    division_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['grc', 'division_name']
