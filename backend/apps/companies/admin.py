from django.contrib import admin

from companies.models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_active', 'location')

admin.site.register(Company, CompanyAdmin)
