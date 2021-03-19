from datetime import datetime

from django.db import models
from django.db.models import Count, Case, When, IntegerField, Q, Value, F
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
            ).values('month', 'user__division__grc__user_department__department_name').annotate(
                total=Count('month')
            ).values(
                'month', 'total', 'user__division__grc__user_department__department_name'
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

    def get_results_with_month_range(self, from_date=None, to_date=None, group_by_department=False):
        """
        get_results_by_month for the past 12 months
        """
        current_month = datetime(datetime.now().year, datetime.now().month, 1)

        if not from_date:
            from_date = current_month - relativedelta(months=11)

        if not to_date:
            to_date = current_month + relativedelta(months=1)

        if group_by_department:
            results = Result.objects.filter(dateCreated__gte=from_date, dateCreated__lt=to_date).annotate(
                month=TruncMonth('dateCreated')
            ).values('month', 'user__division__grc__user_department__department_name').annotate(
                total=Count('month')
            ).values(
                'month', 'total', 'user__division__grc__user_department__department_name'
            )
        else:
            results = Result.objects.filter(dateCreated__gte=from_date, dateCreated__lt=to_date).annotate(
                month=TruncMonth('dateCreated')
            ).values('month').annotate(
                total=Count('month')
            ).values(
                'month', 'total'
            )
        months = []
        while from_date + relativedelta(months=1) <= to_date:
            months.append(from_date.strftime('%Y %m'))
            from_date = from_date + relativedelta(months=1)

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
            ).values('date', 'user__division__grc__user_department__department_name').annotate(
                total=Count('date')
            ).values(
                'date', 'total', 'user__division__grc__user_department__department_name'
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

    def get_results_with_date_range(self, from_date=None, to_date=None, group_by_department=False):
        """
        get results for date range specified
        """
        if group_by_department:
            results = Result.objects.filter(dateCreated__gte=from_date, dateCreated__lt=to_date).annotate(
                date=TruncDate('dateCreated')
            ).values('date', 'user__division__grc__user_department__department_name').annotate(
                total=Count('date')
            ).values(
                'date', 'total', 'user__division__grc__user_department__department_name'
            )
        else:
            results = Result.objects.filter(dateCreated__gte=from_date, dateCreated__lt=to_date).annotate(
                date=TruncDate('dateCreated')
            ).values('date').annotate(
                total=Count('date')
            ).values(
                'date', 'total'
            )

        dates = []
        while from_date + relativedelta(days=1) <= to_date:
            dates.append(from_date.strftime('%d-%m-%Y'))
            from_date = from_date + relativedelta(days=1)

        return results, dates

    def get_total_result_status(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                                filter_department='all'):
        """
        Show total pass and fail
        """
        q = Q(user__is_active=True)
        if from_date:
            q &= Q(dateCreated__gte=from_date)
        if to_date:
            q &= Q(dateCreated__lte=to_date)

        if filter_division != 'all':
            q &= Q(user__division__id=filter_division)
        elif filter_grc != 'all':
            q &= Q(user__division__grc__id=filter_grc)
        elif filter_department != 'all':
            q &= Q(user__division__grc__user_department__id=filter_department)

        results = Result.objects.filter(q).aggregate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        )
        return results

    def group_result_status_by_module(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                                      filter_department='all'):
        """
        Show total pass and fail (group by module)
        """
        q = Q(user__is_active=True)
        if from_date:
            q &= Q(dateCreated__gte=from_date)
        if to_date:
            q &= Q(dateCreated__lte=to_date)

        if filter_division != 'all':
            q &= Q(user__division__id=filter_division)
        elif filter_grc != 'all':
            q &= Q(user__division__grc__id=filter_grc)
        elif filter_department != 'all':
            q &= Q(user__division__grc__user_department__id=filter_department)

        results = Result.objects.filter(q).values('scenario__module').annotate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        ).values('passed', 'failed', 'scenario__module__module_name')
        return results

    def group_result_status_by_scenario(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                                        filter_department='all'):
        """
        Show total pass and fail (group by scenario)
        """
        q = Q(user__is_active=True)
        if from_date:
            q &= Q(dateCreated__gte=from_date)
        if to_date:
            q &= Q(dateCreated__lte=to_date)

        if filter_division != 'all':
            q &= Q(user__division__id=filter_division)
        elif filter_grc != 'all':
            q &= Q(user__division__grc__id=filter_grc)
        elif filter_department != 'all':
            q &= Q(user__division__grc__user_department__id=filter_department)

        results = Result.objects.filter(q).values('scenario').annotate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        ).values('passed', 'failed', 'scenario__module__module_name', 'scenario__scenario_title')
        return results

    def get_critical_failure(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                             filter_department='all', data_type=None, filter_title=None):
        """
        Show total pass and fail (group by scenario)
        """
        q = Q(user__is_active=True)
        if from_date:
            q &= Q(dateCreated__gte=from_date)
        if to_date:
            q &= Q(dateCreated__lte=to_date)

        if filter_division != 'all':
            q &= Q(user__division__id=filter_division)
        elif filter_grc != 'all':
            q &= Q(user__division__grc__id=filter_grc)
        elif filter_department != 'all':
            q &= Q(user__division__grc__user_department__id=filter_department)

        if data_type and filter_title:
            q &= Q(is_pass=False)

            if data_type == 'Modules':
                q &= Q(scenario__module__module_name=filter_title)
            elif data_type == 'Scenarios':
                q &= Q(scenario__scenario_title=filter_title)

        results = Result.objects.filter(q).values(
            'critical_failure'
        ).annotate(
            failure=Case(When(Q(critical_failure__isnull=True) | Q(critical_failure=""), then=Value('Other')),
                         default=F('critical_failure')),
            count=Count(F('failure'))
        ).values('failure', 'count')

        return results


class Result(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spend = models.DurationField(blank=True, null=True)
    results = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    is_pass = models.BooleanField(blank=True, null=True)
    mac_id = models.CharField(max_length=256, default="")
    config = models.TextField(blank=True, null=True)
    passing_score = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    breeding_points = models.TextField(blank=True, null=True)
    breeding_points_found = models.TextField(blank=True, null=True)
    breeding_points_not_found = models.TextField(blank=True, null=True)
    result_breakdown = models.TextField(blank=True, null=True)
    teleport_path = models.TextField(blank=True, null=True)
    critical_failure = models.CharField(max_length=256, null=True, blank=True)
    audio = models.FileField(upload_to='upload/audio', blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = ResultManager()
