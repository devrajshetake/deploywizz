from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Site(models.Model):
    name = models.CharField(max_length=100, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    virtual_machine = models.ForeignKey('automation.VirtualMachine', on_delete=models.CASCADE, default=1)
    jenkins_job = models.OneToOneField('automation.Job', on_delete=models.CASCADE, related_name='associated_site', default=1)

    def __str__(self):
        return self.name

    def deploy(self):
        deployment = Deployment.objects.create(site=self, deployed_at=timezone.now)
        deployment.save()

class Deployment(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, default=1)
    deployed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Deployment for {self.site.name} at {self.deployed_at}"
    