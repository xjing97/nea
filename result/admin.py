from django.contrib import admin

# Register your models here.
from .models import Result

class ResultAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'user', 'time_spend', 'results','is_pass','dateCreated', 'dateUpdated')
    list_filter =('scenario', 'user', 'time_spend', 'results','is_pass','dateCreated', 'dateUpdated')
    search_fields = ('scenario',)
    ordering = ('scenario',)
    filter_horizontal = ()

admin.site.register(Result, ResultAdmin)
