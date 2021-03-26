from django.contrib import admin

# Register your models here.
from .models import Result, ResultBreakdown


class ResultAdmin(admin.ModelAdmin):
    list_display = ('uid', 'scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                    'dateCreated', 'dateUpdated')
    list_filter = ('uid', 'scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                   'dateCreated', 'dateUpdated')
    search_fields = ('uid', 'scenario__scenario_title', 'user__username', 'results', 'is_pass', 'critical_failure')
    ordering = ('-dateCreated',)
    filter_horizontal = ()


class ResultBreakdownAdmin(admin.ModelAdmin):
    list_display = ('id', 'scenario', 'user', 'result', 'event_id', 'event_is_pass', 'is_critical', 'overall_is_pass',
                    'dateCreated', 'dateUpdated')
    list_filter = ('id', 'scenario', 'user', 'result', 'event_id', 'event_is_pass', 'is_critical', 'overall_is_pass',
                   'dateCreated', 'dateUpdated')
    search_fields = ('id', 'scenario__scenario_title', 'user__username', 'result__uid', 'event_id', 'event_is_pass',
                     'is_critical', 'overall_is_pass')
    ordering = ('-dateCreated',)
    filter_horizontal = ()


admin.site.register(Result, ResultAdmin)
admin.site.register(ResultBreakdown, ResultBreakdownAdmin)
