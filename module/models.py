import json

from django.db import models
from django.db.models import Count, Max, F, Case, When, Value, CharField

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

        difficulty = {
            'Easy': {'total': 0, 'latest': None},
            'Medium': {'total': 0, 'latest': None},
            'Hard': {'total': 0, 'latest': None},
            'All': {'total': 0, 'latest': None},
        }
        total = 0
        latest = None
        for module in list(modules):
            difficulty[module['level']] = {'total': module['total'], 'latest': module['latest']}
            total += module['total']
            if not latest:
                latest = module['latest']
            elif module['latest'] > latest:
                latest = module['latest']

        difficulty['All'] = {'total': total, 'latest': latest}

        return difficulty


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
    def get_all_default_configs(self):
        scenarios = Scenario.objects.annotate(
            module_name=F('module__module_name'),
            building_type=F('inspection_site'),
            cover_photo=F('cover_image'),
            passing_score=F('module__passing_score'),
        ).values(
            'id', 'default_config', 'module_name', 'building_type', 'cover_photo', 'description', 'level',
            'scenario_title', 'passing_score'
        )

        return scenarios


class Scenario(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT, related_name='scenario')
    scenario_title = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='upload/scenario')
    # high_rise = models.BooleanField(default=False)
    inspection_site = models.CharField(max_length=256, default="")
    level = models.CharField(choices=LEVEL, max_length=256, default='Easy')
    default_config = models.TextField(default=json.dumps({}))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = ScenarioManager()

    def __str__(self):
        return str(self.module) + "_" + self.inspection_site + "_" + self.level
