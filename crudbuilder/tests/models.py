from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User

# User = get_user_model()


class TestModel(models.Model):

    name = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class TestChildModel(models.Model):
    model = models.ForeignKey(
        TestModel,
        blank=True,
        null=True,
        related_name='children',
        on_delete=CASCADE
    )
