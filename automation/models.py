from django.db import models
from django.contrib.auth.models import User
from sites.models import Site
from api4jenkins import Jenkins


# Create your models here.

class VirtualMachine(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    public_ip = models.CharField(max_length = 24, unique = True)
    provider = models.CharField(max_length = 24) 
    region = models.CharField(max_length = 24)
    cpus = models.IntegerField(null = True, blank = True)
    ram = models.FloatField(null = True, blank = True)
    memory = models.FloatField(null = True, blank = True)
    architecture = models.CharField(max_length = 10, null = True, blank = True)

    def get_public_ip(self):
        return self.public_ip
    
    def set_system_attributes(self, cpus=None, ram=None, memory=None, architecture=None):
        # Set the system attributes if provided
        if cpus is not None:
            self.cpus = cpus
        if ram is not None:
            self.ram = ram
        if memory is not None:
            self.memory = memory
        if architecture is not None:
            self.architecture = architecture
        self.save()

    def get_info(self):
        # Return a dictionary containing information about the virtual machine
        return {
            "id" : self.id,
            "user": self.user.username if self.user else None,
            "public_ip": self.public_ip,
            "provider": self.provider,
            "region": self.region,
            "cpus": self.cpus,
            "ram": self.ram,
            "memory": self.memory,
            "architecture": self.architecture
        }

    @classmethod
    def get_vm_by_user(cls, user):
        # Return a list of virtual machines belonging to the specified user
        return [vm.get_info() for vm in cls.objects.filter(user=user)]
    
    def __str__(self):
        return self.public_ip + ": " + self.user.username




class Job(models.Model):
    site = models.OneToOneField(Site, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length = 64)
    path = models.CharField(max_length = 128, blank = True, default = "")

    def __str__(self):
        return self.name
    
    def create(cls, **kwargs):
        try:
            job = cls.objects.create(**kwargs)
        except:
            pass
        return job



