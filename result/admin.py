from django.contrib import admin

# Register your models here.
from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                    'dateCreated', 'dateUpdated')
    list_filter = ('scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                   'dateCreated', 'dateUpdated')
    search_fields = ('scenario__scenario_title', 'user__username', 'results', 'is_pass', 'critical_failure')
    ordering = ('scenario__scenario_title',)
    filter_horizontal = ()


admin.site.register(Result, ResultAdmin)
