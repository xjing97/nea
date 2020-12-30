from django.contrib import admin

# Register your models here.
from .models import Config

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'breeding_point', 'is_owner_at_home', 'is_owner_appeal','is_refuse_entry', 'critical_points', 'config', 'mac_ids','dateCreated', 'dateUpdated')
    list_filter = ('scenario', 'breeding_point', 'is_owner_at_home', 'is_owner_appeal','is_refuse_entry', 'critical_points', 'config', 'mac_ids','dateCreated', 'dateUpdated')
    search_fields = ('scenario',)
    ordering = ('scenario',)
    filter_horizontal = ()

admin.site.register(Config, ConfigAdmin)
