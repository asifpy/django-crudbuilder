from django.db import models
from django.contrib.auth.models import User


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='%(class)ss_creators',
        on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='%(class)ss_updators',
        on_delete=models.CASCADE)

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

    def __str__(self):
        return self.name

    @property
    def foo(self):
        return self.name


class PersonEmployment(Audit):

    mypk = models.AutoField(primary_key=True)
    year = models.IntegerField()
    salary = models.FloatField()
    person = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    medical_allowance = models.BooleanField(default=False)
