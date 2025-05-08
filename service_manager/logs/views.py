from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated

from logs.models.account_log import AccountLog
from logs.models.log import Log
from logs.serializers import AccountLogSerializer, LogSerializer


class AccountLogListView(generics.ListAPIView):
    serializer_class = AccountLogSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, description="Start datetime", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter("end", openapi.IN_QUERY, description="End datetime", type=openapi.TYPE_STRING, format='date-time'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = AccountLog.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        if start and end:
            queryset = queryset.filter(timestamp__range=(start, end))
        elif start:
            queryset = queryset.filter(timestamp__gte=start)
        elif end:
            queryset = queryset.filter(timestamp__lte=end)

        return queryset


class LogListView(generics.ListAPIView):
    serializer_class = LogSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, description="Start datetime", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter("end", openapi.IN_QUERY, description="End datetime", type=openapi.TYPE_STRING, format='date-time'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Log.objects.all()
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        if start and end:
            queryset = queryset.filter(created_at__range=(start, end))
        elif start:
            queryset = queryset.filter(created_at__gte=start)
        elif end:
            queryset = queryset.filter(created_at__lte=end)

        return queryset


class LogCreateView(generics.CreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class ManagerLogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Log
    template_name = 'logs/manager_log_list.html'
    context_object_name = 'logs'
    ordering = ['-created_at']

    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_manager', False)
