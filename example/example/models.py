from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):

    """ an actual singular human being """
    # model fields
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='creators')
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='updators')
    img = models.ImageField(
        upload_to='uploads',
        blank=True)

    def __unicode__(self):
        return self.name


class PersonEmployment(models.Model):
    year = models.IntegerField()
    salary = models.FloatField()
    person = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        related_name='employments')
    medical_allowance = models.BooleanField(default=False)
