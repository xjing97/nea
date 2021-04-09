import json
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from django.db import models
from django.db.models import Count, Case, When, IntegerField, Q, Value, F, Sum, Max
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
                                filter_department='all', last_attempt_only=False):
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

        if last_attempt_only:
            last_attempt_ids = Result.objects.values('user__id', 'scenario').annotate(
                last_attempt_id=Max(F('id'))
            ).values_list('last_attempt_id', flat=True)

            q &= Q(id__in=last_attempt_ids)

        results = Result.objects.filter(q).aggregate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        )

        return results

    def group_result_status_by_module(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                                      filter_department='all', last_attempt_only=False):
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

        if last_attempt_only:
            last_attempt_ids = Result.objects.values('user__id', 'scenario').annotate(
                last_attempt_id=Max(F('id'))
            ).values_list('last_attempt_id', flat=True)

            q &= Q(id__in=last_attempt_ids)

        results = Result.objects.filter(q).values('scenario__module').annotate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        ).values('passed', 'failed', 'scenario__module__module_name')
        return results

    def group_result_status_by_scenario(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                                        filter_department='all', last_attempt_only=False):
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

        if last_attempt_only:
            last_attempt_ids = Result.objects.values('user__id', 'scenario').annotate(
                last_attempt_id=Max(F('id'))
            ).values_list('last_attempt_id', flat=True)

            q &= Q(id__in=last_attempt_ids)

        results = Result.objects.filter(q).values('scenario').annotate(
            passed=Count(Case(When(is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(is_pass=False, then=1), output_field=IntegerField())),
        ).values('passed', 'failed', 'scenario__module__module_name', 'scenario__scenario_title')
        return results

    def get_critical_failure(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                             filter_department='all', filter_title=None):
        """
        Show total pass and fail (group by scenario)
        """
        q = Q(user__is_active=True)
        q &= Q(is_pass=False)

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

        if filter_title:
            q &= Q(scenario__scenario_title=filter_title)

        overview = Result.objects.filter(q).values(
            'critical_failure'
        ).annotate(
            failure=Case(When(Q(critical_failure__isnull=True) | Q(critical_failure=""), then=Value('Other')),
                         default=F('critical_failure')),
            count=Count(F('failure'))
        ).values('failure', 'count')

        failure_dict = {}

        failure_list = list(Result.objects.filter(q).filter(critical_failure__isnull=False).exclude(
            critical_failure=""
        ).values_list('critical_failure', flat=True))

        scenario = Scenario.objects.filter(scenario_title=filter_title).first()
        config = json.loads(scenario.default_config) if scenario.default_config else None

        if config:
            scrips_list = config['Scenario']
            if scrips_list:
                for script in scrips_list:
                    events = script["Events"]
                    if events:
                        for event in events:
                            if event["Event_ID"] in failure_list:
                                failure_dict[event["Event_ID"]] = event["Hint"]

        details = Result.objects.filter(q).annotate(
            user_department=F('user__division__grc__user_department__department_name'),
            grc=F('user__division__grc__grc_name'),
            division=F('user__division__division_name'),
        ).values('id', 'uid', 'user_department', 'grc', 'division', 'results', 'critical_failure', 'dateCreated')

        return overview, details, failure_dict


class Result(models.Model):
    uid = models.CharField(unique=True, default=uuid.uuid4, max_length=256)
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spend = models.CharField(blank=True, null=True, max_length=10)
    results = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    user_scores = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    total_scores = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
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

    def __str__(self):
        return self.uid

    def update_result_breakdown(self, result_breakdown, scores, user_scores):
        breakdown_str = self.result_breakdown
        breakdown_json = None
        if breakdown_str:
            breakdown_json = json.loads(breakdown_str)

        for breakdown in result_breakdown:
            result_breakdown_obj = ResultBreakdown.objects.filter(
                result__uid=self.uid, event_id=breakdown['event_id'], script_id=breakdown['script_id']
            ).first()

            result_breakdown_obj.user_event_scores = breakdown['user_event_scores']

            score_percentage = Decimal(breakdown['user_event_scores']) / Decimal(result_breakdown_obj.total_event_scores) * 100

            keyword_passing_score = self.get_keyword_passing_score()

            if keyword_passing_score and score_percentage < keyword_passing_score:
                result_breakdown_obj.event_is_pass = False
            else:
                result_breakdown_obj.event_is_pass = True

            result_breakdown_obj.save()

            if breakdown_json:
                for b in breakdown_json:
                    if 'Script_ID' in b:
                        if b['Script_ID'] == result_breakdown_obj.script_id and b['Event_ID'] == result_breakdown_obj.event_id:
                            b['score'] = result_breakdown_obj.user_event_scores
                    elif b['Event_ID'] == result_breakdown_obj.event_id:
                            b['score'] = result_breakdown_obj.user_event_scores

                self.result_breakdown = json.dumps(breakdown_json)

        if scores:
            self.results = scores
            self.user_scores = user_scores
            if not self.critical_failure:
                if scores >= self.passing_score:
                    self.is_pass = True
                else:
                    self.is_pass = False
            else:
                self.is_pass = False
        self.save()
        
    def create_result_breakdown(self):
        if self.result_breakdown:
            breakdowns = json.loads(self.result_breakdown)
            if breakdowns:
                for breakdown in breakdowns:
                    if self.config:
                        if 'Script_ID' in breakdown:
                            event = self.get_event_info_from_config(breakdown['Event_ID'], breakdown['Script_ID'])
                        else:
                            event = self.get_event_info_from_config(breakdown['Event_ID'])

                        if event:
                            action_performed = None
                            if breakdown['Action'] == 'True':
                                action_performed = True
                            elif breakdown['Action'] == 'False':
                                action_performed = False

                            keyword_spoken = None
                            if breakdown['Speech'] != 'None':
                                keyword_spoken = breakdown['Speech']

                            try:
                                dt = datetime.strptime(breakdown['Event_Time'], '%H:%M:%S')
                                time_spent = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
                            except Exception as ex:
                                print(ex)
                                time_spent = timedelta(hours=0, minutes=0, seconds=0)

                            event_is_pass = True
                            if event['total_event_scores'] and 'score' in breakdown:
                                event_percentage = int(breakdown['score']) / event['total_event_scores'] * 100
                                keyword_passing_score = self.get_keyword_passing_score()
                                if keyword_passing_score and event_percentage < keyword_passing_score:
                                    event_is_pass = False

                                ResultBreakdown.objects.create(
                                    result=self, scenario=self.scenario, user=self.user, script_id=event['script_id'],
                                    scene_name=event['scene_name'], event_id=event['event_id'],
                                    event_type=event['event_type'], description=event['description'],
                                    event_keywords=event['event_keywords'], action_performed=action_performed,
                                    keywords_spoken=keyword_spoken, user_location=breakdown['teleport_location'],
                                    time_spent=time_spent, user_event_scores=int(breakdown['score']),
                                    total_event_scores=event['total_event_scores'], event_is_pass=event_is_pass,
                                    is_critical=event['is_critical_point'], overall_is_pass=self.is_pass
                                )

    def get_event_info_from_config(self, event_id, script_id=None):
        try:
            scenario_config = json.loads(self.config)["Scenario"]
            if scenario_config:
                if script_id:
                    scenario = next(filter(lambda x: x['Script_ID'] == script_id, scenario_config), None)

                    if scenario:
                        event = next(filter(lambda x: x['Event_ID'] == event_id, scenario['Events']), None)

                        if event:
                            scores = 0
                            event_type = 'Action'
                            keywords = []
                            for action in event['Action']:
                                scores += int(action['Score'] if 'Score' in action else 0)
                                if action['Type'] == 'Speech':
                                    event_type = 'Speech'
                                    keywords.append(action['Keywords'])

                            return {
                                'script_id': scenario['Script_ID'],
                                'scene_name': scenario['Scenario_Title'],
                                'event_id': event['Event_ID'],
                                'description': event['Hint'],
                                'event_type': event_type,
                                'event_keywords': json.dumps(keywords),
                                'total_event_scores': scores,
                                'is_critical_point': True if event['Is_Critical_Point'] == 'True' or event[
                                    'Is_Critical_Point'] is True else False
                            }
                else:
                    event = next(filter(lambda event: event['event'], map(lambda x: {
                        'Scenario_Title': x['Scenario_Title'],
                        'Script_ID': x['Script_ID'],
                        'event': next(filter(lambda y: y['Event_ID'] == event_id, x['Events']), None)
                    }, scenario_config)), None)

                    if event:
                        scores = 0
                        event_type = 'Action'
                        keywords = []
                        for action in event['event']['Action']:
                            scores += int(action['Score'] if 'Score' in action else 0)
                            if action['Type'] == 'Speech':
                                event_type = 'Speech'
                                keywords.append(action['Keywords'])

                        return {
                            'script_id': event['Script_ID'],
                            'scene_name': event['Scenario_Title'],
                            'event_id': event['event']['Event_ID'],
                            'description': event['event']['Hint'],
                            'event_type': event_type,
                            'event_keywords': json.dumps(keywords),
                            'total_event_scores': scores,
                            'is_critical_point': True if event['event']['Is_Critical_Point'] == 'True' or
                                                         event['event']['Is_Critical_Point'] is True else False
                        }

            return None
        except Exception as ex:
            print(ex)
            return None

    def get_keyword_passing_score(self):
        if self.config:
            config_json = json.loads(self.config)

            if config_json:
                init_config = config_json['Init']
                if init_config:
                    keyword_passing_score = Decimal(init_config['Speech_Confident_Level_Pass_Level']) * 100
                    return keyword_passing_score
        return None


class ResultBreakdownManager(models.Manager):
    def get_event_analysis(self, from_date=None, to_date=None, filter_division='all', filter_grc='all',
                           filter_department='all', filter_title=None, critical_only=False, last_attempt_only=False):
        """
        Show total pass and fail of each event (group by event id)
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

        if filter_title:
            q &= Q(scenario__scenario_title=filter_title)

        if critical_only:
            q &= Q(is_critical=True)

        if last_attempt_only:
            last_attempt_ids = Result.objects.values('user__id', 'scenario').annotate(
                last_attempt_id=Max(F('id'))
            ).values_list('last_attempt_id', flat=True)

            q &= Q(result__id__in=last_attempt_ids)

        event_info = ResultBreakdown.objects.filter(q).values('event_id', 'script_id').annotate(
            event_pass=Sum(Case(When(event_is_pass=True, then=Value(1)), default=Value(0)),
                           output_field=IntegerField()),
            event_fail=Sum(Case(When(event_is_pass=False, then=Value(1)), default=Value(0)),
                           output_field=IntegerField()),
        ).values('event_id', 'script_id', 'event_pass', 'event_fail')

        for eve in event_info:
            latest_event = ResultBreakdown.objects.filter(
                event_id=eve['event_id'], script_id=eve['script_id'], scenario__scenario_title=filter_title
            ).latest('dateCreated')
            if latest_event:
                eve['descp'] = latest_event.description
            else:
                eve['descp'] = ""

        return event_info


class ResultBreakdown(models.Model):
    result = models.ForeignKey(Result, on_delete=models.PROTECT)
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    script_id = models.CharField(max_length=256, default="")
    scene_name = models.CharField(max_length=256, default="")
    event_id = models.CharField(max_length=256, default="")
    event_type = models.CharField(max_length=256, default="")
    description = models.TextField(blank=True, null=True)
    event_keywords = models.CharField(max_length=256, default="")
    action_performed = models.BooleanField(max_length=256, blank=True, null=True, default=None)
    keywords_spoken = models.CharField(max_length=256, blank=True, null=True, default=None)
    user_location = models.CharField(max_length=256, default="")
    time_spent = models.DurationField(blank=True, null=True)
    user_event_scores = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    total_event_scores = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
    event_is_pass = models.BooleanField(blank=True, null=True, default=None)
    is_critical = models.BooleanField(blank=True, null=True, default=None)
    overall_is_pass = models.BooleanField(blank=True, null=True, default=None)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    objects = ResultBreakdownManager()
