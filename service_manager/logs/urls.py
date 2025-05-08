from django.urls import path

from logs.views import (
    LogCreateView,
    LogListView,
    ManagerLogListView,
    AccountLogListView
)

app_name = 'logs'

urlpatterns = [
    # Log URLs
    path('logs/', LogListView.as_view(), name='log-list'),
    path('logs/create/', LogCreateView.as_view(), name='log-create'),
    path('manager-logs/', ManagerLogListView.as_view(), name='manager-log-list'),
    path('account-logs/', AccountLogListView.as_view(), name='account-log-list'),
]
