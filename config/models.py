import json

from django.db import models

from module.models import Scenario


class ConfigManager(models.Manager):
    pass


class Config(models.Model):
    scenario_id = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    breeding_point = models.TextField(blank=True, null=True)
    is_owner_at_home = models.BooleanField(default=True)
    is_owner_appeal = models.BooleanField(default=False)
    is_refuse_entry = models.BooleanField(default=False)
    critical_points = models.TextField(blank=True, null=True)
    config = models.TextField(default=json.dumps({}))
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
