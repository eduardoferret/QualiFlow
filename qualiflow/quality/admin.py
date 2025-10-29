from django.contrib import admin

from . import models


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('created_at',)


@admin.register(models.Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'created_at')
    search_fields = ('name', 'branch__name', 'branch__code')
    list_filter = ('branch',)


class DocumentVersionInline(admin.TabularInline):
    model = models.DocumentVersion
    extra = 0


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'sector', 'current_version', 'created_at')
    search_fields = ('title', 'branch__name', 'sector__name')
    list_filter = ('branch', 'sector')
    inlines = [DocumentVersionInline]


@admin.register(models.Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'sector', 'created_by', 'created_at')
    search_fields = ('name', 'branch__name', 'sector__name')
    list_filter = ('branch', 'sector')


class WorkflowStepInline(admin.TabularInline):
    model = models.WorkflowStep
    extra = 0


@admin.register(models.Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'workflow', 'branch', 'sector', 'status', 'created_at')
    search_fields = ('name', 'workflow__name')
    list_filter = ('status', 'branch', 'sector')


@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = (
        'process',
        'workflow_step',
        'status',
        'assigned_to',
        'started_at',
        'completed_at',
    )
    list_filter = ('status', 'workflow_step__workflow')
    search_fields = (
        'process__name',
        'workflow_step__name',
        'assigned_to__username',
    )


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'branch',
        'sector',
        'process',
        'assigned_to',
        'status',
        'priority',
        'due_date',
    )
    list_filter = ('status', 'priority', 'branch', 'sector')
    search_fields = ('title', 'process__name', 'assigned_to__username')
