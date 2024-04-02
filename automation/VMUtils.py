from .models import VirtualMachine
import paramiko
class VMUtils():
    def __init__(self, vm : VirtualMachine) -> None:
        self.vm = vm
        try: 
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.file_path = "/home/dev/Desktop/BE Project/VMs/tests/BYOVM1_key.pem"

            private_key_string = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

            # Create an RSAKey object from the private key string
            # private_key = paramiko.RSAKey.from_private_key(paramiko.RSAKey.transport.load_openssh_private_key(private_key_string))
            private_key = paramiko.PKey(data=private_key_string)

            

            self.client.connect(hostname=self.vm.public_ip, username="azureuser", key_filename="/home/dev/Desktop/BE Project/VMs/tests/BYOVM1_key.pem")


            # Execute the ls command
            # Execute commands to gather system information
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

            print( {
                "CPU Cores": cpu_cores,
                "Total Disk Size": disk_size,
                "RAM": round(float(ram[:-2])),
                "Architecture": architecture
            })
    


        except Exception as e:
            raise Exception("Error connecting the VM: " + str(e))

    
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



