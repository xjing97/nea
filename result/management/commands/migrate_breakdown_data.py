import json
from datetime import datetime, timedelta
from functools import reduce

from django.core.management import BaseCommand

from result.models import Result, ResultBreakdown


class Command(BaseCommand):
    def handle(self, **args):
        ResultBreakdown.objects.all().delete()
        results = Result.objects.all()

        for result in results:
            if result.result_breakdown:
                breakdowns = json.loads(result.result_breakdown)
                if breakdowns:
                    for breakdown in breakdowns:
                        if result.config:
                            if 'Script_ID' in breakdown:
                                event = result.get_event_info_from_config(breakdown['Event_ID'], breakdown['Script_ID'])
                            else:
                                event = result.get_event_info_from_config(breakdown['Event_ID'])

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
                                    keyword_passing_score = result.get_keyword_passing_score()
                                    if keyword_passing_score and event_percentage < keyword_passing_score:
                                        event_is_pass = False

                                    breakdown_obj = ResultBreakdown.objects.create(
                                        result=result, scenario=result.scenario, user=result.user, script_id=event['script_id'],
                                        scene_name=event['scene_name'], event_id=event['event_id'],
                                        event_type=event['event_type'], description=event['description'],
                                        event_keywords=event['event_keywords'], action_performed=action_performed,
                                        keywords_spoken=keyword_spoken, user_location=breakdown['teleport_location'],
                                        time_spent=time_spent, user_event_scores=int(breakdown['score']),
                                        total_event_scores=event['total_event_scores'], event_is_pass=event_is_pass,
                                        is_critical=event['is_critical_point'], overall_is_pass=result.is_pass
                                    )
                                    print("Created breakdown for ", breakdown_obj.script_id, " ", breakdown_obj.event_id)

                                    # mock date created
                                    breakdown_obj.dateCreated = result.dateCreated
                                    breakdown_obj.save()
