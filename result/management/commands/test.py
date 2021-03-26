from datetime import datetime, timedelta

from django.core.management import BaseCommand

from result.models import Result, ResultBreakdown


class Command(BaseCommand):
    def handle(self, **args):
        ResultBreakdown.objects.get_event_info_chart(2, True)
