import json
from datetime import datetime, timedelta
from pathlib import Path

import openpyxl
from django.core.management import BaseCommand

from core.models import User
from module.models import Scenario
from result.models import Result, ResultBreakdown


class Command(BaseCommand):
    def handle(self, **args):
        ResultBreakdown.objects.all().delete()
        Result.objects.all().delete()

        with open('C:/Users/AVPL/Desktop/consolidate_result.json') as f:
            results = json.loads(f.read())

            for data in results:
                user = User.objects.filter(username=data['user__username'], soeId=data['user__soeId']).first()
                scenario = None
                if data['scenario__scenario_title']:
                    scenario = Scenario.objects.filter(scenario_title=data['scenario__scenario_title']).first()

                if scenario and user:
                    result = Result.objects.filter(
                        uid=data['uid']
                    ).first()
                    if not result:
                        result = Result.objects.create(uid=data['uid'], scenario=scenario, user=user)
                        print(result, ' is created')

                        result.breeding_points = data['breeding_points']
                        result.breeding_points_found = data['breeding_points_found']
                        result.breeding_points_not_found = data['breeding_points_not_found']

                        result.time_spend = data['time_spend']
                        result.start_time = data['start_time']
                        result.end_time = data['end_time']
                        result.results = data['results']
                        result.is_pass = data['is_pass']
                        result.critical_failure = data['critical_failure']
                        result.is_completed = True if data['is_completed_str'] == 'Completed' else False
                        result.dateCreated = data['dateCreated']

                        result.user_scores = data['user_scores']
                        result.total_scores = data['total_scores']
                        result.mac_id = data['mac_id']
                        result.config = data['config']
                        result.passing_score = data['passing_score']
                        result.teleport_path = data['teleport_path']
                        result.result_breakdown = data['result_breakdown']
                        # result.dateCreated = row[18].value
                        result.save()
                        result.create_result_breakdown()
                        print(result.uid, " result breakdown is created")
                    else:
                        print(result.id, ' is exists')
