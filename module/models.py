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
    passingScore = models.FloatField(default=50.0)
    quizCanRetake = models.BooleanField(default=False)
    quizAttempt = models.IntegerField(default=1)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)


class ScenarioManager(models.Manager):
    pass


class Scenario(models.Model):
    module_id = models.ForeignKey(Module, on_delete=models.PROTECT)
    user_id = models.ManyToManyField(User)
    description = models.TextField(blank=True, null=True)
    coverImage = models.ImageField(upload_to='upload/scenario')
    highRise = models.BooleanField(default=False)
    level = models.CharField(choices=LEVEL, max_length=256, default='Easy')
    defaultConfig = models.TextField(default=json.dumps({}))
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
