from django.contrib import admin
from .models import Task, Category, Profile, Group, Event, EventParticipation, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'task_count']
    list_filter = ['parent']
    search_fields = ['name']
    ordering = ['parent__name', 'name']
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'priority', 'completed', 'due_date', 'created_at']
    list_filter = ['completed', 'priority', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['completed_at', 'created_at', 'updated_at']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'balance', 'spending_limit', 'is_verified']
    list_filter = ['is_verified', 'can_create_groups', 'can_join_events']
    search_fields = ['user__username', 'student_id', 'trusted_adult_email']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'is_public', 'is_active']
    list_filter = ['is_public', 'is_active', 'requires_approval']
    search_fields = ['name', 'description', 'creator__username']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'creator', 'start_datetime', 'total_cost', 'status']
    list_filter = ['status', 'requires_payment', 'start_datetime']
    search_fields = ['title', 'description', 'creator__username', 'group__name']

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'payment_status', 'amount_paid', 'attendance_status']
    list_filter = ['payment_status', 'attendance_status', 'joined_at']
    search_fields = ['user__username', 'event__title']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'amount', 'transaction_type', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'description']
    readonly_fields = ['id', 'created_at', 'processed_at']