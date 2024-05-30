from django.db import models
from django.contrib.auth.models import User
# from sites.models import Site
from api4jenkins import Jenkins
# from .VMUtils import VMUtils
import paramiko
import requests


# Create your models here.

class VirtualMachine(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    public_ip = models.CharField(max_length = 24, unique = True)
    provider = models.CharField(max_length = 24) 
    region = models.CharField(max_length = 24)
    cpus = models.CharField(max_length = 10,null = True, blank = True)
    ram = models.CharField(max_length = 10,null = True, blank = True)
    memory = models.CharField(max_length = 10,null = True, blank = True)
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
    
    def deploy(self, git_url):
        # Deploy a site to the virtual machine
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            file_path = "C:\\Users\\dshetake\\OneDrive - Avaya\\Desktop\\cicd\\deploy\\deploywizz\\keys\\id_rsa"
            pkey = paramiko.RSAKey.from_private_key_file(file_path)
            client.connect(hostname=self.public_ip, username="root", pkey=pkey, look_for_keys=False)
            # stdin, stdout, stderr = client.exec_command(f'git clone {git_url}')
            # stdin, stdout, stderr = client.exec_command(f"git clone {git_url} && cd {git_url.split('/')[-1]} && docker-compose build && docker-compose up -d")
            # stdin, stdout, stderr = client.exec_command(f"if [ ! -d {git_url.split('/')[-1]} ]; then git clone {git_url} && cd {git_url.split('/')[-1]} && docker-compose build && docker-compose up -d; fi")
            repo_name = git_url.split('/')[-1].replace('.git', '')

            command = f"""
            if [ ! -d {repo_name} ]; then 
            git clone {git_url}; 
            fi && 
            cd {repo_name} && 
            docker-compose build && 
            docker-compose up -d
            """
            stdin, stdout, stderr = client.exec_command(command)

            stdout = stdout.read().decode()
            stderr = stderr.read().decode()

            print(stdout, stderr)

            client.close()
            return f"{stdout}\n\n{stderr}"
        except Exception as e:
            print(e)
            return f"Error deploying site: {str(e)}"
        
    def add_dns_record(self, subdomain, ip):
        # Add a DNS record for the virtual machine
        # Define the API endpoint and domain
        url = 'https://api.godaddy.com/v1/domains/pictieee.in/records'

        # Define the data payload
        payload = [{
            'data': ip,
            'name': subdomain,
            'ttl': 3600,
            'type': 'A'
        }]

        # Define the headers
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'sso-key e42poj24tVXr_BLuJyviJ92B2qMLMBHB5zy:3RuE7qiLrRBdSRHqC9myh7'
        }

        # Make the PATCH request
        response = requests.patch(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return "DNS record updated successfully"
        else:
            print(response.content)
            return f"Failed to update DNS record. Status code: {response.status_code}"
        
    
    def __str__(self):
        return self.public_ip + ": " + self.user.username




class Job(models.Model):
    site = models.OneToOneField('sites.Site', on_delete = models.CASCADE, null = True)
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



