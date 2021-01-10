from datetime import datetime

from django.core.management import BaseCommand

from result.models import Result


class Command(BaseCommand):
    def handle(self, **args):
        result = Result.objects.create(scenario_id=2, user_id=2, time_spend=datetime.now(), results=30, is_pass=False)
        result.dateCreated = datetime(2020, 10, 11)
        result.save()
