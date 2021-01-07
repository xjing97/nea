from datetime import datetime

from django.db import models
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import TruncMonth, TruncDate
from dateutil.relativedelta import relativedelta

from core.models import User
from module.models import Scenario


class ResultManager(models.Manager):
    def get_results_by_month(self, group_by_department=False):
        """
        get_results_by_month for the past 12 months
        """
        current_month = datetime(datetime.now().year, datetime.now().month, 1)
        next_month = current_month + relativedelta(months=1)
        prev_12_months = current_month - relativedelta(months=11)

        if group_by_department:
            results = Result.objects.filter(dateCreated__gte=prev_12_months, dateCreated__lt=next_month).annotate(
                month=TruncMonth('dateCreated')
            ).values('month', 'user__department').annotate(
                total=Count('month')
            ).values(
                'month', 'total', 'user__department'
            )
        else:
            results = Result.objects.filter(dateCreated__gte=prev_12_months, dateCreated__lt=next_month).annotate(
                month=TruncMonth('dateCreated')
            ).values('month').annotate(
                total=Count('month')
            ).values(
                'month', 'total'
            )
        months = []
        while prev_12_months + relativedelta(months=1) <= next_month:
            months.append(prev_12_months.strftime('%Y %m'))
            prev_12_months = prev_12_months + relativedelta(months=1)

        return results, months

    def get_results_by_date(self, month=datetime(datetime.now().year, datetime.now().month, 1), group_by_department=False):
        """
        get_results_by_date of the month (default: current month)
        month example: datetime(2020, 12, 1)
        """
        one_month = month + relativedelta(months=1)
        if group_by_department:
            results = Result.objects.filter(dateCreated__gte=month, dateCreated__lt=one_month).annotate(
                date=TruncDate('dateCreated')
            ).values('date', 'user__department').annotate(
                total=Count('date')
            ).values(
                'date', 'total', 'user__department'
            )
        else:
            results = Result.objects.filter(dateCreated__gte=month, dateCreated__lt=one_month).annotate(
                date=TruncDate('dateCreated')
            ).values('date').annotate(
                total=Count('date')
            ).values(
                'date', 'total'
            )
        return results

    def get_total_result_status(self):
        """
        Show total pass and fail
        """
        results = Result.objects.aggregate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        )
        return results

    def group_result_status_by_module(self):
        """
        Show total pass and fail (group by module)
        """
        results = Result.objects.values('scenario__module').annotate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        ).values('passed', 'failed', 'scenario__module__module_name')
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
