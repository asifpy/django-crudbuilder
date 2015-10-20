from django.db import models


class Person(models.Model):

    """ an actual singular human being """
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return self.name