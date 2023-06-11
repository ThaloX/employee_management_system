from django.contrib import admin

from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('password',)
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser',)
    readonly_fields = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(EmployeeDetails)
admin.site.register(EmployeeEducation)
admin.site.register(EmployeeExperience)
