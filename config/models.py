import json

from django.db import models
from django.db.models import Count, When, F, Case, Value , IntegerField, BooleanField, Q

from config.constants import ALL_MAC_IDS
from module.models import Scenario
from result.models import Result


class ConfigManager(models.Manager):
    def get_config_by_macid(self, user_id, mac_id):
        # check quiz can be retake or not and user's attempt
        attended_modules = Result.objects.filter(
            user__id=user_id
        ).values(
            'scenario__module__id'
        ).annotate(
            attempt=Count('scenario__module__id')
        )

        attended_dict = {}
        for module in list(attended_modules):
            attended_dict[module['scenario__module__id']] = module['attempt']

        whens = [
            When(scenario__module__id=k, then=v) for k, v in attended_dict.items()
        ]
        config = Config.objects.filter(
            (Q(mac_ids__contains=mac_id) | Q(mac_ids__contains=ALL_MAC_IDS)) & Q(date_deleted__isnull=True)
        ).annotate(
            module_name=F('scenario__module__module_name'),
            building_type=F('scenario__inspection_site'),
            cover_photo=F('scenario__cover_image'),
            description=F('scenario__description'),
            level=F('scenario__level'),
            scenario_title=F('scenario__scenario_title'),
            quiz_attempt=F('scenario__quiz_attempt'),
            user_attempt=Case(*whens, default=0, output_field=IntegerField()),
        ).annotate(
            user_can_attend=Case(
                When(user_attempt__lt=F('scenario__quiz_attempt'), then=Value(True)),
                default=Value(False), output_field=BooleanField()
            ),
        ).values(
            'id', 'config', 'module_name', 'building_type', 'cover_photo', 'description', 'level',
            'scenario_title', 'passing_score', 'user_can_attend', 'quiz_attempt', 'user_attempt'
        )
        return config


class Config(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    breeding_point = models.TextField(blank=True, null=True)
    config = models.TextField(default=json.dumps({}))
    mac_ids = models.TextField(default=json.dumps([]))
    passing_score = models.FloatField(default=80.0)
    date_deleted = models.DateTimeField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = ConfigManager()
