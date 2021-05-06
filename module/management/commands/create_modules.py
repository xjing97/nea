import json
from datetime import datetime

from django.core.management import BaseCommand

from module.models import Module, Scenario
from result.models import Result


class Command(BaseCommand):
    def handle(self, **args):
        module1, created = Module.objects.get_or_create(module_name='Vector Control Module', description='')

        hdbScenario = Scenario.objects.create(module=module1, scenario_title='Vector Inspection (HDB)',
                                              inspection_site='HDB', cover_image='upload/scenario/hdb.png',
                                              default_config=open('module/json/hdb.json').read().encode(
                                                  'cp1252').decode('utf-8'))
        hdbScenario.save()

        landedScenario = Scenario.objects.create(module=module1, scenario_title='Vector Inspection (Landed)',
                                                 inspection_site='Landed', cover_image='upload/scenario/landed.png',
                                                 default_config=open('module/json/landed.json').read().encode(
                                                     'cp1252').decode('utf-8'))
        landedScenario.save()
