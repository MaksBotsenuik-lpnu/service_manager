from django.db import models


class Log(models.Model):
    user = models.ForeignKey(
        'authenticate.User', on_delete=models.CASCADE, related_name="logs"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs_logs'
