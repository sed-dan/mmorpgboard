from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class UserCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def code_valid(self):
        return self.created_at > timezone.now() - timedelta(minutes=10)
