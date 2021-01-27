from django.contrib import admin

# Register your models here.
from .models import Module, Scenario


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'description', 'quiz_can_retake', 'quiz_attempt', 'date_created',
                    'date_updated')
    list_filter = ('module_name', 'quiz_can_retake', 'quiz_attempt', 'date_created', 'date_updated')
    search_fields = ('module_name',)
    ordering = ('module_name',)
    filter_horizontal = ()


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('module', 'scenario_title', 'description', 'cover_image', 'inspection_site', 'date_created',
                    'date_updated')
    list_filter = ('module', 'scenario_title', 'description', 'cover_image', 'inspection_site', 'date_created',
                   'date_updated')
    search_fields = ('module',)
    ordering = ('module',)
    filter_horizontal = ()


admin.site.register(Module, ModuleAdmin)
admin.site.register(Scenario, ScenarioAdmin)
