from .models import VirtualMachine
import paramiko
class VMUtils():
    def __init__(self, vm : VirtualMachine, file_path : str = None) -> None:
        self.vm = vm
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.file_path = file_path

    
    def get_system_info(self):
        try:
            self.client.connect(hostname=self.vm.public_ip, username="azureuser", key_filename=self.file_path)

            stdin, stdout, stderr = self.client.exec_command('nproc')
            cpu_cores = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('df -h --total | grep "total" | awk \'{print $2}\'')
            disk_size = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('free -h | awk \'/^Mem/ {print $2}\'')
            ram = stdout.read().decode().strip()

            stdin, stdout, stderr = self.client.exec_command('uname -m')
            architecture = stdout.read().decode().strip()

            # Close client connection
            self.client.close()

            return {
                "cpu_cores": cpu_cores,
                "disk_size": disk_size,
                "ram": ram,
                "architecture": architecture
            }
        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e))
        
    def setup(self):
        try:
            self.client.connect(hostname=self.vm.public_ip, username="azureuser", key_filename=self.file_path)

            stdin, stdout, stderr = self.client.exec_command('add setup command here') # Change
        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e))


# C:\Users\dshetake\OneDrive - Avaya\Desktop\cicd\deploy\test1_vm.pem



