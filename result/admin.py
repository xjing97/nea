from django.contrib import admin

# Register your models here.
from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = ('uid', 'scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                    'dateCreated', 'dateUpdated')
    list_filter = ('uid', 'scenario', 'user', 'time_spend', 'results', 'is_pass', 'critical_failure',
                   'dateCreated', 'dateUpdated')
    search_fields = ('uid', 'scenario__scenario_title', 'user__username', 'results', 'is_pass', 'critical_failure')
    ordering = ('-dateCreated',)
    filter_horizontal = ()


admin.site.register(Result, ResultAdmin)
