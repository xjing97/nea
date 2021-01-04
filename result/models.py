from datetime import datetime

from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDate
from dateutil.relativedelta import relativedelta

from core.models import User
from module.models import Scenario


class ResultManager(models.Manager):
    def get_results_by_month(self):
        """
        get_results_by_month for the past 12 months
        """
        current_month = datetime(datetime.now().year, datetime.now().month, 1)
        next_month = current_month + relativedelta(months=1)
        prev_12_months = current_month - relativedelta(months=11)
        results = Result.objects.filter(dateCreated__gte=prev_12_months, dateCreated__lt=next_month).annotate(
            month=TruncMonth('dateCreated')
        ).values('month').annotate(
            total=Count('month')
        ).values(
            'month', 'total'
        )
        return results

    def get_results_by_date(self, month=datetime(datetime.now().year, datetime.now().month, 1)):
        """
        get_results_by_date of the month (default: current month)
        month example: datetime(2020, 12, 1)
        """
        one_month = month + relativedelta(months=1)
        results = Result.objects.filter(dateCreated__gte=month, dateCreated__lt=one_month).annotate(
            date=TruncDate('dateCreated')
        ).values('date').annotate(
            total=Count('date')
        ).values(
            'date', 'total'
        )
        return results


class Result(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time_spend = models.TimeField(blank=True, null=True)
    results = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    is_pass = models.BooleanField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = ResultManager()
