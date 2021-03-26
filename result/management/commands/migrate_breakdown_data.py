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
                            print(result.id)
                            # event = result.get_event_info_from_config(breakdown['Event_ID'])
                            event = self.get_event_info_from_config(result, breakdown['Event_ID'])

                            if event:
                                print(event)

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
                                    if event_percentage < result.passing_score:
                                        event_is_pass = False

                                    breakdown_obj = ResultBreakdown.objects.create(
                                        result=result, scenario=result.scenario, user=result.user,
                                        scene_name=event['scene_name'], event_id=event['event_id'],
                                        event_type=event['event_type'], description=event['description'],
                                        event_keywords=event['event_keywords'], action_performed=action_performed,
                                        keywords_spoken=keyword_spoken, user_location=breakdown['teleport_location'],
                                        time_spent=time_spent, user_event_scores=int(breakdown['score']),
                                        total_event_scores=event['total_event_scores'], event_is_pass=event_is_pass,
                                        is_critical=event['is_critical_point'], overall_is_pass=result.is_pass
                                    )

    def get_event_info_from_config(self, result, event_id, scenario_id=None):
        try:
            scenario_config = json.loads(result.config)["Scenario"]
            if scenario_config:
                if scenario_id:
                    scenario = next(filter(lambda x: x['Script_ID'] == scenario_id, scenario_config), None)

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
                                'scene_name': scenario['Scenario_Title'],
                                'event_id': event['Event_ID'],
                                'description': event['Hint'],
                                'event_type': event_type,
                                'event_keywords': keywords,
                                'total_event_scores': scores,
                                'is_critical_point': True if event['Is_Critical_Point'] == 'True' or event[
                                    'Is_Critical_Point'] is True else False
                            }
                else:
                    event = next(filter(lambda event: event['event'], map(lambda x: {
                        'Scenario_Title': x['Scenario_Title'],
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
                            'scene_name': event['Scenario_Title'],
                            'event_id': event['event']['Event_ID'],
                            'description': event['event']['Hint'],
                            'event_type': event_type,
                            'event_keywords': keywords,
                            'total_event_scores': scores,
                            'is_critical_point': True if event['event']['Is_Critical_Point'] == 'True' or
                                                         event['event']['Is_Critical_Point'] is True else False
                        }

            return None
        except Exception as ex:
            print(ex)
            return None
