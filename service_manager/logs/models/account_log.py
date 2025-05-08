from django.db import models


class AccountLog(models.Model):
    user = models.ForeignKey(
        'authenticate.User', on_delete=models.SET_NULL, null=True, related_name="account_logs"
    )
    action = models.TextField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 