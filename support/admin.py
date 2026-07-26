from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'short_message', 'source', 'status', 'admin_notified', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'source', 'admin_notified', 'created_at']
    search_fields = ['name', 'email', 'message']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    readonly_fields = ['name', 'email', 'message', 'source', 'conversation',
                       'user', 'admin_notified', 'created_at']

    fieldsets = (
        ('Who', {'fields': ('name', 'email', 'user', 'source')}),
        ('Message', {'fields': ('message', 'conversation')}),
        ('Handling', {'fields': ('status', 'admin_notified', 'created_at')}),
    )

    actions = ['mark_in_progress', 'mark_resolved']

    def has_add_permission(self, request):
        return False  # contacts only ever arrive from the site

    @admin.action(description='Mark selected as In Progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='Mark selected as Resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')
