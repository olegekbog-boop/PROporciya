from django.contrib import admin
from .models import Company, Contact, Pipeline, Stage, Deal, Activity

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'assigned_to', 'created_at']
    list_filter = ['created_at', 'assigned_to']
    search_fields = ['name', 'phone', 'email']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'phone', 'email']
    list_filter = ['company']
    search_fields = ['first_name', 'last_name', 'phone', 'email']

@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_by', 'created_at']

class StageInline(admin.TabularInline):
    model = Stage
    extra = 1

@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_by', 'created_at']
    inlines = [StageInline]

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'stage', 'amount', 'priority', 'assigned_to', 'created_at']
    list_filter = ['stage', 'priority', 'created_at']
    search_fields = ['title', 'company__name']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'company', 'due_date', 'completed', 'created_by']
    list_filter = ['type', 'completed', 'due_date']
    search_fields = ['title', 'company__name']
