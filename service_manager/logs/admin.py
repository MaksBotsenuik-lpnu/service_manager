from django.contrib import admin

from logs.models.log import Log
from logs.models.account_log import AccountLog


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)


@admin.register(AccountLog)
class AccountLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'description')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
