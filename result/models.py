from django.db import models

from core.models import User
from module.models import Scenario


class ResultManager(models.Manager):
    pass


class Result(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time_spend = models.TimeField(blank=True, null=True)
    results = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    is_pass = models.BooleanField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
