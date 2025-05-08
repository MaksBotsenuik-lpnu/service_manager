from logs.models.log import Log

def create_log(user, message):
    if user and user.is_authenticated:
        Log.objects.create(user=user, message=message) 