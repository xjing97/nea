import json

from django.db import models

# Create your models here.
from core.models import User
from module.constants import LEVEL


class ModuleManager(models.Manager):
    pass


class Module(models.Model):
    module_name = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True, null=True)
    passing_score = models.FloatField(default=50.0)
    quiz_can_retake = models.BooleanField(default=False)
    quiz_attempt = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class ScenarioManager(models.Manager):
    pass


class Scenario(models.Model):
    module_id = models.ForeignKey(Module, on_delete=models.PROTECT)
    user_id = models.ManyToManyField(User)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='upload/scenario')
    high_rise = models.BooleanField(default=False)
    level = models.CharField(choices=LEVEL, max_length=256, default='Easy')
    default_config = models.TextField(default=json.dumps({}))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
