from datetime import datetime, timedelta

from django.core.management import BaseCommand

from result.models import Result


class Command(BaseCommand):
    def handle(self, **args):
        result = Result.objects.create(scenario_id=2, user_id=2, time_spend=timedelta(hours=1, minutes=2), results=30, is_pass=False)
        result.dateCreated = datetime(2020, 10, 11)
        result.save()
