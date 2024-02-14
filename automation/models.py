from django.db import models
from sites import Site

# Create your models here.
class Job(models.Model):
    site = models.OneToOneField()