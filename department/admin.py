from django.contrib import admin

# Register your models here.
from .models import Division, GRC, UserDepartment


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'grc', 'division_name', 'date_created', 'date_updated')
    list_filter = ('division_name', 'date_created', 'date_updated')
    search_fields = ('division_name',)
    ordering = ('division_name',)
    filter_horizontal = ()


class GRCAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_department', 'grc_name', 'date_created', 'date_updated')
    list_filter = ('grc_name', 'date_created', 'date_updated')
    search_fields = ('grc_name',)
    ordering = ('grc_name',)
    filter_horizontal = ()


class UserDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name', 'date_created', 'date_updated')
    list_filter = ('department_name', 'date_created', 'date_updated')
    search_fields = ('department_name',)
    ordering = ('department_name',)
    filter_horizontal = ()


admin.site.register(Division, DivisionAdmin)
admin.site.register(GRC, GRCAdmin)
admin.site.register(UserDepartment, UserDepartmentAdmin)
