from django.db import models
from django.contrib.auth.models import User


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='%(class)ss_creators')
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='%(class)ss_updators')

    class Meta:
        abstract = True


class Person(Audit):

    """ an actual singular human being """
    # model fields
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    img = models.ImageField(
        upload_to='uploads',
        blank=True)

    def __unicode__(self):
        return self.name


class PersonEmployment(Audit):
    year = models.IntegerField()
    salary = models.FloatField()
    person = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        related_name='employments')
    medical_allowance = models.BooleanField(default=False)
