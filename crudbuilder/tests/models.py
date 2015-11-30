from django.db import models
from django.contrib.auth.models import User

# User = get_user_model()


class TestModel(models.Model):

    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, null=True)
