from django.contrib import admin

from .models import Job, Application

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'employment_type', 'vacancy')
    list_filter = ('company',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'applicant', 'applied_at', 'status')
    list_display_links = ('id', 'job')
    ordering = ('-id',)

    
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
