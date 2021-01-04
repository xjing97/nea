import json

from django.db import models
from django.db.models import Count, Max

from module.constants import LEVEL


class ModuleManager(models.Manager):
    def get_all_modules(self):
        modules = list(Module.objects.values('id', 'module_name', 'date_created', 'date_updated'))
        for module in modules:
            scenarios = Scenario.objects.filter(module__id=module['id']).values()
            module['scenarios'] = list(scenarios)

        return modules

    def count_modules_by_difficulty(self):
        modules = Scenario.objects.values(
            'level'
        ).annotate(
            total=Count('level'),
            latest=Max('date_updated')
        ).values('total', 'level', 'latest')

        return modules


class Module(models.Model):
    module_name = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True, null=True)
    passing_score = models.FloatField(default=50.0)
    quiz_can_retake = models.BooleanField(default=False)
    quiz_attempt = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = ModuleManager()

    def __str__(self):
        return self.module_name


class ScenarioManager(models.Manager):
    pass


class Scenario(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name='scenario')
    scenario_title = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='upload/scenario')
    high_rise = models.BooleanField(default=False)
    level = models.CharField(choices=LEVEL, max_length=256, default='Easy')
    default_config = models.TextField(default=json.dumps({}))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.module) + ("_highrise_" if self.high_rise else "_lowrise_") + self.level
