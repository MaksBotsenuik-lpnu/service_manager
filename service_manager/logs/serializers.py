from rest_framework import serializers
from logs.models.log import Log
from logs.models.account_log import AccountLog


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'user', 'message', 'created_at']


class AccountLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLog
        fields = '__all__'
