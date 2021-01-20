from datetime import datetime

from django.core.management import BaseCommand

from module.models import Module, Scenario


class Command(BaseCommand):
    def handle(self, **args):
        module1 = Module.objects.create(module_name='Module 1', description='This is module 1', passing_score=60,
                                       quiz_can_retake=True, quiz_attempt=2)
        module1.date_created = datetime(2021, 1, 3)
        module1.save()
        module2 = Module.objects.create(module_name='Module 2', description='This is module 2', passing_score=60,
                                       quiz_can_retake=False, quiz_attempt=1)
        module2.date_created = datetime(2021, 1, 4)
        module2.save()

        scenario1 = Scenario.objects.create(module=module1, scenario_title='Scenario 1 for module 1',
                                            description='This is scenario 1 for module 1', inspection_site='HDB',
                                            level='Easy')
        scenario1.date_created = datetime(2021, 1, 3)
        scenario1.save()

        scenario2 = Scenario.objects.create(module=module1, scenario_title='Scenario 2 for module 1',
                                            description='This is scenario 2 for module 1', inspection_site='Landed',
                                            level='Medium')
        scenario2.date_created = datetime(2021, 1, 5)
        scenario2.save()

        scenario3 = Scenario.objects.create(module=module2, scenario_title='Scenario 1 for module 2',
                                            description='This is scenario 1 for module 2', inspection_site='Landed',
                                            level='Hard')
        scenario3.date_created = datetime(2021, 1, 6)
        scenario3.save()
